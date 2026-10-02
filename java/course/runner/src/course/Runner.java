package course;

import java.io.*;
import java.lang.reflect.*;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

/**
 * Compiles and runs learner code inside the browser (CheerpJ), or locally for tests.
 *
 * Usage: Runner <sourceDir> <outDir> <mode: run|check> [timeoutMs]
 *   sourceDir  folder with Main.java (and Check.java in check mode) and optional stdin.txt
 *   outDir     fresh folder for compiled classes
 *
 * Output protocol (lines starting with @@ are for the page, not the learner):
 *   @@COMPILE_ERROR / @@RUNTIME_ERROR / @@TIMEOUT / @@PASS / @@FAIL <message> / @@DONE <ms>
 */
public final class Runner {
    static final PrintStream REAL_OUT = System.out;
    static final PrintStream REAL_ERR = System.err;
    static ClassLoader loader;
    static String mainClassName = "Main";
    static String stdinText = "";
    static String lastSource = "";
    static String lastSource() { return lastSource; }

    public static void main(String[] args) throws Exception {
        String src = args[0], out = args[1], mode = args.length > 2 ? args[2] : "run";
        long timeout = args.length > 3 ? Long.parseLong(args[3]) : 10000;
        NO_POOL = args.length > 4 && args[4].equals("nopool");
        if (NO_POOL) { if (POOL != null && !(POOL instanceof Boolean)) REAL_POOL = POOL; POOL = Boolean.FALSE; }
        else if (POOL instanceof Boolean && REAL_POOL != null) POOL = REAL_POOL;
        else if (POOL instanceof Boolean) POOL = null;
        long t0 = System.currentTimeMillis();
        try {
            run(src, out, mode, timeout);
        } finally {
            System.setOut(REAL_OUT);
            System.setErr(REAL_ERR);
            REAL_OUT.println("@@DONE " + (System.currentTimeMillis() - t0) + " compile=" + compileMs + " pool=" + (POOL == null ? "none" : POOL.getClass().getSimpleName()));
            REAL_OUT.flush();
        }
    }

    /**
     * src is either a folder containing Main.java / Check.java / stdin.txt, or a flat prefix such as
     * /str/job7 with files job7.main, job7.check and job7.stdin (CheerpJ's /str/ has no subfolders).
     * Sources are copied into out/src so javac sees files named after their classes.
     */
    static void run(String src, String out, String mode, long timeout) throws Exception {
        String code = readSource(src, "Main.java", ".main");
        String checkCode = mode.equals("check") ? readSource(src, "Check.java", ".check") : null;
        String stdin = readSource(src, "stdin.txt", ".stdin");
        stdinText = stdin == null ? "" : stdin;
        if (code == null) throw new FileNotFoundException("No source found at " + src);
        lastSource = code;
        mainClassName = findMainClass(code);
        Map<String, String> sources = new LinkedHashMap<>();
        sources.put(mainClassName + ".java", code);
        if (checkCode != null) sources.put("Check.java", checkCode);
        if (!compileInMemory(sources)) return;

        loader = new MemLoader(Runner.class.getClassLoader());
        Thread.currentThread().setContextClassLoader(loader);

        if (mode.equals("javap")) {
            disassemble(out);
            return;
        }
        if (mode.equals("run")) {
            runMain(stdinText, timeout, true);
        } else {
            String output = runMain(stdinText, timeout, true);
            if (output == null) {
                REAL_OUT.println("@@FAIL Your program has to run without errors before it can be checked. Fix the error above and try again.");
                return;
            }
            T.output = output;
            try {
                Class<?> check = Class.forName("Check", true, loader);
                Method m = check.getMethod("run");
                if (timeout > 0) runWithTimeout(() -> m.invoke(null), timeout); else m.invoke(null);
                REAL_OUT.println("@@PASS");
            } catch (Throwable e) {
                Throwable c = unwrap(e);
                if (c instanceof T.Fail) {
                    REAL_OUT.println("@@FAIL " + c.getMessage().replace("\n", "\\n"));
                } else if (c instanceof TimeoutError) {
                    REAL_OUT.println("@@FAIL Checking took too long. Is there an endless loop in your code?");
                } else {
                    REAL_OUT.println("@@FAIL Checking your code raised " + describe(c));
                }
            }
        }
    }

    /** Writes the compiled classes to disk and prints `javap -c -p` for each one (the Bytecode tab). */
    static void disassemble(String outDir) throws Exception {
        Path dir = Paths.get(outDir, "classes" + System.nanoTime());
        Files.createDirectories(dir);
        List<String> files = new ArrayList<>();
        List<String> names = new ArrayList<>(CLASS_BYTES.keySet());
        Collections.sort(names);
        names.remove(mainClassName);
        names.add(0, mainClassName);
        for (String name : names) {
            Path f = dir.resolve(name.replace('.', '_') + ".class");
            Files.write(f, CLASS_BYTES.get(name));
            files.add(f.toString());
        }
        java.util.spi.ToolProvider javap = java.util.spi.ToolProvider.findFirst("javap").orElse(null);
        if (javap == null) {
            for (java.util.spi.ToolProvider t : ServiceLoader.load(java.util.spi.ToolProvider.class, Runner.class.getClassLoader()))
                if (t.name().equals("javap")) javap = t;
        }
        if (javap == null) { err("@@RUNTIME_ERROR", "The bytecode viewer isn't available."); return; }
        StringWriter sw = new StringWriter();
        PrintWriter pw = new PrintWriter(sw);
        List<String> args = new ArrayList<>(List.of("-c", "-p"));
        args.addAll(files);
        javap.run(pw, pw, args.toArray(new String[0]));
        pw.flush();
        String text = sw.toString().replaceAll("(?m)^Compiled from \"[^\"]*\"\\R", "");
        REAL_OUT.println("@@JAVAP_BEGIN");
        REAL_OUT.print(text);
        REAL_OUT.println("@@JAVAP_END");
        for (String f : files) Files.deleteIfExists(Paths.get(f));
        Files.deleteIfExists(dir);
    }

    static String readSource(String src, String folderName, String suffix) throws IOException {
        Path a = Paths.get(src, folderName);
        if (Files.isRegularFile(a)) return new String(Files.readAllBytes(a), StandardCharsets.UTF_8);
        Path b = Paths.get(src + suffix);
        try {
            return new String(Files.readAllBytes(b), StandardCharsets.UTF_8);
        } catch (IOException e) {
            return null;
        }
    }

    static String findMainClass(String code) {
        String noComments = code.replaceAll("(?s)/\\*.*?\\*/", "").replaceAll("//[^\\n]*", "");
        java.util.regex.Matcher m = java.util.regex.Pattern.compile("public\\s+(?:final\\s+|abstract\\s+)*class\\s+(\\w+)").matcher(noComments);
        if (m.find()) return m.group(1);
        m = java.util.regex.Pattern.compile("(?:class|record|enum|interface)\\s+(\\w+)").matcher(noComments);
        return m.find() ? m.group(1) : "Main";
    }

    // ---- in-memory compilation (no disk writes; compiler and file manager stay warm between runs) ----
    static javax.tools.JavaCompiler COMPILER;
    static javax.tools.StandardJavaFileManager STD_FM;
    static final Map<String, byte[]> CLASS_BYTES = new HashMap<>();
    static javax.tools.JavaFileManager MEM_FM;
    static Object POOL;            // com.sun.tools.javac.api.JavacTaskPool when available, else Boolean.FALSE
    static Object REAL_POOL;
    static boolean NO_POOL;

    /** Compiles with javac's JavacTaskPool (reuses compiler state between runs, as JShell does) when available. */
    static boolean pooledCompile(javax.tools.DiagnosticCollector<javax.tools.JavaFileObject> diags, List<String> options,
                                 List<javax.tools.JavaFileObject> units) throws Exception {
        if (Boolean.getBoolean("course.nopool") || NO_POOL) POOL = Boolean.FALSE;
        if (POOL == null) {
            try {
                POOL = Class.forName("com.sun.tools.javac.api.JavacTaskPool").getConstructor(int.class).newInstance(1);
            } catch (Throwable e) {
                POOL = Boolean.FALSE;
            }
        }
        if (POOL instanceof Boolean) {
            return COMPILER.getTask(null, MEM_FM, diags, options, null, units).call();
        }
        Class<?> worker = Class.forName("com.sun.tools.javac.api.JavacTaskPool$Worker");
        Object w = java.lang.reflect.Proxy.newProxyInstance(worker.getClassLoader(), new Class<?>[]{worker}, (proxy, method, args) -> {
            if (!method.getName().equals("withTask")) return method.invoke(proxy, args);
            return ((javax.tools.JavaCompiler.CompilationTask) args[0]).call();
        });
        Method getTask = POOL.getClass().getMethod("getTask", Writer.class, javax.tools.JavaFileManager.class,
                javax.tools.DiagnosticListener.class, Iterable.class, Iterable.class, Iterable.class, worker);
        try {
            return (Boolean) getTask.invoke(POOL, null, MEM_FM, diags, options, null, units, w);
        } catch (InvocationTargetException e) {
            throw (e.getCause() instanceof Exception) ? (Exception) e.getCause() : e;
        }
    }
    static long compileMs, runMs;

    static final class Src extends javax.tools.SimpleJavaFileObject {
        final String code;
        Src(String fileName, String code) {
            super(java.net.URI.create("string:///" + fileName), Kind.SOURCE);
            this.code = code;
        }
        @Override public CharSequence getCharContent(boolean ignoreEncodingErrors) { return code; }
    }

    static final class Out extends javax.tools.SimpleJavaFileObject {
        final String name;
        Out(String name) {
            super(java.net.URI.create("mem:///" + name.replace('.', '/') + ".class"), Kind.CLASS);
            this.name = name;
        }
        @Override public OutputStream openOutputStream() {
            return new ByteArrayOutputStream() {
                @Override public void close() throws IOException { super.close(); CLASS_BYTES.put(name, toByteArray()); }
            };
        }
    }

    static final class MemLoader extends ClassLoader {
        MemLoader(ClassLoader parent) { super(parent); }
        @Override protected Class<?> findClass(String name) throws ClassNotFoundException {
            byte[] b = CLASS_BYTES.get(name);
            if (b == null) throw new ClassNotFoundException(name);
            return defineClass(name, b, 0, b.length);
        }
    }

    static boolean compileInMemory(Map<String, String> sources) throws Exception {
        long t = System.currentTimeMillis();
        if (COMPILER == null) {
            COMPILER = javax.tools.ToolProvider.getSystemJavaCompiler();
            if (COMPILER == null) {
                Class<?> k = Class.forName("com.sun.tools.javac.api.JavacTool");
                COMPILER = (javax.tools.JavaCompiler) k.getMethod("create").invoke(null);
            }
            STD_FM = COMPILER.getStandardFileManager(null, Locale.ENGLISH, StandardCharsets.UTF_8);
            String runnerJar = Runner.class.getProtectionDomain().getCodeSource().getLocation().getPath();
            STD_FM.setLocation(javax.tools.StandardLocation.CLASS_PATH, List.of(new File(runnerJar)));
        }
        CLASS_BYTES.clear();
        if (MEM_FM == null) {
            MEM_FM = new javax.tools.ForwardingJavaFileManager<javax.tools.JavaFileManager>(STD_FM) {
                @Override public javax.tools.JavaFileObject getJavaFileForOutput(Location loc, String className, javax.tools.JavaFileObject.Kind kind, javax.tools.FileObject sibling) {
                    return new Out(className);
                }
            };
        }
        List<javax.tools.JavaFileObject> units = new ArrayList<>();
        for (Map.Entry<String, String> e : sources.entrySet()) units.add(new Src(e.getKey(), e.getValue()));
        javax.tools.DiagnosticCollector<javax.tools.JavaFileObject> diags = new javax.tools.DiagnosticCollector<>();
        List<String> options = new ArrayList<>(List.of("-encoding", "UTF-8", "-Xlint:-options", "-Xmaxerrs", "8"));
        String release = System.getProperty("course.release");
        if (release != null) { options.add("--release"); options.add(release); }
        boolean ok = pooledCompile(diags, options, units);
        compileMs = System.currentTimeMillis() - t;
        StringBuilder msg = new StringBuilder();
        int errors = 0;
        for (javax.tools.Diagnostic<? extends javax.tools.JavaFileObject> d : diags.getDiagnostics()) {
            if (d.getKind() != javax.tools.Diagnostic.Kind.ERROR && ok) continue;
            if (d.getKind() == javax.tools.Diagnostic.Kind.ERROR) errors++;
            String file = d.getSource() == null ? "" : d.getSource().getName().replaceFirst("^/", "");
            msg.append(file).append(':').append(d.getLineNumber()).append(": ")
               .append(d.getKind() == javax.tools.Diagnostic.Kind.ERROR ? "error" : "warning").append(": ")
               .append(d.getMessage(Locale.ENGLISH).replace("java.lang.", "")).append('\n');
            if (d.getSource() != null && d.getLineNumber() > 0) {
                String[] lines = sources.getOrDefault(file, "").split("\\R", -1);
                int ln = (int) d.getLineNumber();
                if (ln <= lines.length) {
                    msg.append(lines[ln - 1]).append('\n');
                    long col = d.getColumnNumber();
                    if (col > 0) msg.append(" ".repeat((int) Math.min(col - 1, 300))).append("^\n");
                }
            }
        }
        if (!ok) {
            msg.append(errors).append(errors == 1 ? " error" : " errors").append('\n');
            err("@@COMPILE_ERROR", friendlyCompile(msg.toString()));
            return false;
        }
        return true;
    }

    /** Prints a marker line, then an error block, on standard output so the page sees one ordered stream. */
    static void err(String marker, String text) {
        REAL_OUT.println(marker);
        REAL_OUT.println("@@ERR_BEGIN");
        REAL_OUT.print(text.endsWith("\n") ? text : text + "\n");
        REAL_OUT.println("@@ERR_END");
        REAL_OUT.flush();
    }

    static String friendlyCompile(String msg) {
        if (msg.contains("Check.java")) {
            return "Your code compiled, but the checker couldn't use it. Make sure the class and method names match the exercise.\n" + msg;
        }
        return msg;
    }

    /** Runs the learner's main method with the given input. Returns captured stdout, or null if it failed. */
    static String runMain(String input, long timeout, boolean echo) {
        ByteArrayOutputStream buf = new ByteArrayOutputStream();
        PrintStream tee = new PrintStream(new OutputStream() {
            public void write(int b) { buf.write(b); if (echo) REAL_OUT.write(b); }
            public void write(byte[] b, int off, int len) { buf.write(b, off, len); if (echo) REAL_OUT.write(b, off, len); }
            public void flush() { if (echo) REAL_OUT.flush(); }
        }, true, StandardCharsets.UTF_8);
        System.setIn(new ByteArrayInputStream(input.getBytes(StandardCharsets.UTF_8)));
        System.setOut(tee);
        try {
            Class<?> c = Class.forName(mainClassName, true, loader);
            Method m;
            try {
                m = c.getMethod("main", String[].class);
            } catch (NoSuchMethodException e) {
                err("@@RUNTIME_ERROR", "Class " + mainClassName + " has no main method. Add: public static void main(String[] args) { ... }");
                return null;
            }
            long t = System.currentTimeMillis();
            if (timeout > 0) runWithTimeout(() -> m.invoke(null, (Object) new String[0]), timeout);
            else m.invoke(null, (Object) new String[0]);
            runMs = System.currentTimeMillis() - t;
            tee.flush();
            return buf.toString(StandardCharsets.UTF_8);
        } catch (Throwable e) {
            tee.flush();
            Throwable c = unwrap(e);
            if (c instanceof TimeoutError) {
                err("\n@@TIMEOUT", "Stopped: your program ran for more than " + (timeout / 1000) + " seconds. Is there an endless loop?");
            } else if (c instanceof NoSuchElementException && input.isEmpty()) {
                err("@@RUNTIME_ERROR", "Your program tried to read input, but the Input box is empty. Type one line per value it reads.");
            } else {
                err("@@RUNTIME_ERROR", trace(c));
            }
            return null;
        } finally {
            System.setOut(REAL_OUT);
        }
    }

    static final class TimeoutError extends RuntimeException {
        TimeoutError() { super("timeout"); }
    }

    interface Task { void run() throws Throwable; }

    @SuppressWarnings({"deprecation", "removal"})
    static void runWithTimeout(Task task, long timeout) throws Throwable {
        final Throwable[] err = new Throwable[1];
        Thread t = new Thread(() -> {
            try { task.run(); } catch (Throwable e) { err[0] = e; }
        }, "main");
        t.setDaemon(true);
        t.setContextClassLoader(loader);
        t.start();
        t.join(timeout);
        if (t.isAlive()) {
            try { t.stop(); } catch (Throwable ignored) { }
            throw new TimeoutError();
        }
        if (err[0] != null) throw err[0];
    }

    static Throwable unwrap(Throwable e) {
        while ((e instanceof InvocationTargetException || e instanceof ExceptionInInitializerError) && e.getCause() != null) e = e.getCause();
        return e;
    }

    static String describe(Throwable e) {
        return e.getClass().getSimpleName() + (e.getMessage() != null ? ": " + e.getMessage() : "");
    }

    /** A stack trace showing only the learner's own frames, with repeated frames collapsed. */
    static String trace(Throwable e) {
        StringBuilder sb = new StringBuilder("Exception in thread \"main\" ").append(e.getClass().getName());
        if (e.getMessage() != null) sb.append(": ").append(e.getMessage());
        sb.append('\n');
        String last = null;
        int repeats = 0, shown = 0;
        for (StackTraceElement f : e.getStackTrace()) {
            String cls = f.getClassName();
            if (cls.startsWith("course.") || cls.startsWith("java.lang.reflect") || cls.startsWith("jdk.internal") || cls.startsWith("sun.reflect") || cls.equals("java.lang.Thread")) continue;
            boolean mine = f.getFileName() != null && f.getFileName().endsWith(".java") && !cls.startsWith("java.") && !cls.startsWith("javax.");
            if (!mine && !(cls.startsWith("java.") || cls.startsWith("javax."))) continue;
            String line = "\tat " + f;
            if (line.equals(last)) { repeats++; continue; }
            if (repeats > 0) { sb.append("\t... repeated ").append(repeats).append(repeats == 1 ? " more time\n" : " more times\n"); repeats = 0; }
            if (shown++ >= 25) { sb.append("\t...\n"); break; }
            sb.append(line).append('\n');
            last = line;
        }
        if (repeats > 0) sb.append("\t... repeated ").append(repeats).append(" more times\n");
        if (e.getCause() != null && e.getCause() != e) sb.append("Caused by: ").append(describe(e.getCause())).append('\n');
        if (shown == 0) sb.append("\n(The in-browser Java runtime doesn't report line numbers. Add System.out.println calls to see how far your program gets.)\n");
        return sb.toString();
    }
}
