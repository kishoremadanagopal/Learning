package course;

import java.lang.reflect.*;
import java.util.*;

/** Helpers for exercise checks. Checks are written as: public class Check { public static void run() { ... } } */
public final class T {
    public static String output = "";

    public static final class Fail extends RuntimeException {
        public Fail(String m) { super(m); }
    }

    private T() { }

    // ---- output ----
    public static String output() { return output; }
    public static List<String> lines() {
        String s = output.strip();
        return s.isEmpty() ? List.of() : Arrays.asList(s.split("\\R"));
    }
    /** Runs main again with different input and returns what it printed. */
    public static String runWith(String input) {
        String o = Runner.runMain(input, 10000, false);
        if (o == null) fail("Your program crashed when given the input:\n" + input);
        return o;
    }

    // ---- assertions ----
    public static void fail(String msg) { throw new Fail(msg); }
    public static void check(boolean ok, String msg) { if (!ok) fail(msg); }
    public static void eq(Object expected, Object actual, String what) {
        if (!same(expected, actual)) fail(what + " should be " + show(expected) + " but was " + show(actual));
    }
    public static void near(double expected, Object actual, String what) {
        double a = actual instanceof Number ? ((Number) actual).doubleValue() : Double.NaN;
        if (Math.abs(a - expected) > 1e-6) fail(what + " should be " + expected + " but was " + show(actual));
    }
    public static void outputIs(String expected) {
        String got = output.strip().replace("\r\n", "\n");
        if (!got.equals(expected.strip())) fail("Your program should print:\n" + expected.strip() + "\n\nbut it printed:\n" + (got.isEmpty() ? "(nothing)" : got));
    }
    public static String source() { return Runner.lastSource(); }
    public static void sourceHas(String text, String msg) { if (!Runner.lastSource().contains(text)) fail(msg); }
    public static void sourceLacks(String text, String msg) { if (Runner.lastSource().contains(text)) fail(msg); }

    static boolean same(Object e, Object a) {
        if (e == null || a == null) return e == a;
        if (e instanceof Number && a instanceof Number) {
            if (e instanceof Double || e instanceof Float || a instanceof Double || a instanceof Float)
                return Math.abs(((Number) e).doubleValue() - ((Number) a).doubleValue()) < 1e-9;
            return ((Number) e).longValue() == ((Number) a).longValue();
        }
        if (e.getClass().isArray() && a.getClass().isArray()) return Objects.deepEquals(e, a);
        if (e instanceof List && a instanceof List) {
            List<?> x = (List<?>) e, y = (List<?>) a;
            if (x.size() != y.size()) return false;
            for (int i = 0; i < x.size(); i++) if (!same(x.get(i), y.get(i))) return false;
            return true;
        }
        if (e instanceof Character && a instanceof String) return a.equals(e.toString());
        return e.equals(a);
    }
    public static String show(Object o) {
        if (o == null) return "null";
        if (o instanceof String) return "\"" + o + "\"";
        if (o instanceof Character) return "'" + o + "'";
        if (o instanceof int[]) return Arrays.toString((int[]) o);
        if (o instanceof double[]) return Arrays.toString((double[]) o);
        if (o instanceof long[]) return Arrays.toString((long[]) o);
        if (o instanceof boolean[]) return Arrays.toString((boolean[]) o);
        if (o instanceof char[]) return Arrays.toString((char[]) o);
        if (o instanceof Object[]) return Arrays.deepToString((Object[]) o);
        return String.valueOf(o);
    }

    // ---- reflection: call learner code without compile-time links ----
    public static Class<?> cls(String name) {
        try { return Class.forName(name, true, Runner.loader); }
        catch (ClassNotFoundException e) { throw new Fail("Couldn't find a class named " + name + ". Check the spelling and capitalisation."); }
    }
    public static boolean hasClass(String name) {
        try { Class.forName(name, false, Runner.loader); return true; } catch (ClassNotFoundException e) { return false; }
    }
    /** Calls a static method on the main class. */
    public static Object call(String method, Object... args) { return callStatic(Runner.mainClassName, method, args); }
    public static Object callStatic(String className, String method, Object... args) {
        Class<?> c = cls(className);
        Method m = findMethod(c, method, args, true);
        return invoke(m, null, args, method);
    }
    /** Calls an instance method on an object. */
    public static Object callOn(Object target, String method, Object... args) {
        Method m = findMethod(target.getClass(), method, args, false);
        return invoke(m, target, args, method);
    }
    /** Creates an object with a matching constructor. */
    public static Object make(String className, Object... args) {
        Class<?> c = cls(className);
        for (Constructor<?> k : c.getDeclaredConstructors()) {
            if (fits(k.getParameterTypes(), args)) {
                try { k.setAccessible(true); return k.newInstance(convert(k.getParameterTypes(), args)); }
                catch (InvocationTargetException e) {
                    Fail f = new Fail("Creating a " + className + " threw " + Runner.describe(e.getCause()));
                    f.initCause(e.getCause());
                    throw f;
                }
                catch (Exception e) { throw new Fail("Couldn't create a " + className + ": " + e); }
            }
        }
        throw new Fail(className + " needs a constructor that takes " + describeArgs(args) + ".");
    }
    /** Expects calling the code to throw an exception of the given simple name. */
    public static Throwable expectThrows(String exceptionName, Runnable code, String what) {
        try { code.run(); }
        catch (Fail f) {
            if (f.getCause() != null && f.getCause().getClass().getSimpleName().equals(exceptionName)) return f.getCause();
            throw f;
        }
        catch (Throwable t) {
            Throwable c = Runner.unwrap(t);
            if (matches(c.getClass(), exceptionName)) return c;
            fail(what + " should throw " + exceptionName + " but threw " + c.getClass().getSimpleName());
        }
        fail(what + " should throw " + exceptionName + " but nothing was thrown");
        return null;
    }
    static boolean matches(Class<?> c, String name) {
        for (Class<?> k = c; k != null; k = k.getSuperclass()) if (k.getSimpleName().equals(name)) return true;
        return false;
    }
    public static Object field(Object target, String name) {
        for (Class<?> c = target.getClass(); c != null; c = c.getSuperclass()) {
            try { Field f = c.getDeclaredField(name); f.setAccessible(true); return f.get(target); }
            catch (NoSuchFieldException ignored) { }
            catch (IllegalAccessException e) { throw new Fail(e.toString()); }
        }
        throw new Fail(target.getClass().getSimpleName() + " has no field named " + name);
    }
    public static void setField(Object target, String name, Object value) {
        for (Class<?> c = target.getClass(); c != null; c = c.getSuperclass()) {
            try {
                Field f = c.getDeclaredField(name);
                f.setAccessible(true);
                Object v = value;
                if (f.getType() == double.class && value instanceof Number) v = ((Number) value).doubleValue();
                if (f.getType() == int.class && value instanceof Number) v = ((Number) value).intValue();
                f.set(target, v);
                return;
            } catch (NoSuchFieldException ignored) {
            } catch (IllegalAccessException e) {
                throw new Fail(e.toString());
            }
        }
        throw new Fail(target.getClass().getSimpleName() + " has no field named " + name);
    }
    public static boolean fieldIsPrivate(String className, String name) {
        try { return Modifier.isPrivate(cls(className).getDeclaredField(name).getModifiers()); }
        catch (NoSuchFieldException e) { throw new Fail(className + " has no field named " + name); }
    }
    public static boolean isSubclass(String child, String parent) { return cls(parent).isAssignableFrom(cls(child)); }

    static Method findMethod(Class<?> c, String name, Object[] args, boolean wantStatic) {
        List<Method> candidates = new ArrayList<>();
        for (Class<?> k = c; k != null; k = k.getSuperclass()) candidates.addAll(Arrays.asList(k.getDeclaredMethods()));
        for (Class<?> i : allInterfaces(c)) candidates.addAll(Arrays.asList(i.getMethods()));
        boolean nameSeen = false;
        for (Method m : candidates) {
            if (!m.getName().equals(name)) continue;
            nameSeen = true;
            if (fits(m.getParameterTypes(), args)) {
                if (wantStatic && !Modifier.isStatic(m.getModifiers())) throw new Fail("Make " + name + " static: public static ... " + name + "(...)");
                m.setAccessible(true);
                return m;
            }
        }
        String where = c.getSimpleName();
        if (nameSeen) throw new Fail(where + "." + name + " should take " + describeArgs(args) + ".");
        throw new Fail("Couldn't find a method named " + name + " in " + where + ". Check the spelling and capitalisation.");
    }
    static Set<Class<?>> allInterfaces(Class<?> c) {
        Set<Class<?>> s = new LinkedHashSet<>();
        for (Class<?> k = c; k != null; k = k.getSuperclass()) for (Class<?> i : k.getInterfaces()) { s.add(i); s.addAll(allInterfaces(i)); }
        return s;
    }
    static Object invoke(Method m, Object target, Object[] args, String name) {
        try { return m.invoke(target, convert(m.getParameterTypes(), args)); }
        catch (InvocationTargetException e) {
            Fail f = new Fail(name + "(" + argsText(args) + ") threw " + Runner.describe(e.getCause()));
            f.initCause(e.getCause());
            throw f;
        }
        catch (IllegalAccessException e) { throw new Fail("Make " + name + " public."); }
    }
    static String argsText(Object[] args) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < args.length; i++) { if (i > 0) sb.append(", "); sb.append(show(args[i])); }
        return sb.toString();
    }
    static String describeArgs(Object[] args) {
        if (args.length == 0) return "no arguments";
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < args.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(args[i] == null ? "a value" : typeName(args[i].getClass()));
        }
        return sb.toString();
    }
    static String typeName(Class<?> c) {
        if (c == Integer.class) return "an int";
        if (c == Double.class) return "a double";
        if (c == Long.class) return "a long";
        if (c == Boolean.class) return "a boolean";
        if (c == Character.class) return "a char";
        if (c == String.class) return "a String";
        if (c == int[].class) return "an int[]";
        if (c == String[].class) return "a String[]";
        return "a " + c.getSimpleName();
    }
    static final Map<Class<?>, Class<?>> BOX = Map.of(int.class, Integer.class, double.class, Double.class, long.class, Long.class,
            boolean.class, Boolean.class, char.class, Character.class, float.class, Float.class, short.class, Short.class, byte.class, Byte.class);
    static boolean fits(Class<?>[] params, Object[] args) {
        if (params.length != args.length) return false;
        for (int i = 0; i < params.length; i++) {
            Class<?> p = params[i];
            Object a = args[i];
            if (a == null) { if (p.isPrimitive()) return false; continue; }
            Class<?> want = p.isPrimitive() ? BOX.get(p) : p;
            if (want.isInstance(a)) continue;
            if ((p == double.class || p == Double.class) && (a instanceof Integer || a instanceof Long)) continue;
            if ((p == long.class || p == Long.class) && a instanceof Integer) continue;
            return false;
        }
        return true;
    }
    static Object[] convert(Class<?>[] params, Object[] args) {
        Object[] out = args.clone();
        for (int i = 0; i < params.length; i++) {
            Class<?> p = params[i];
            if (out[i] instanceof Number && (p == double.class || p == Double.class)) out[i] = ((Number) out[i]).doubleValue();
            else if (out[i] instanceof Integer && (p == long.class || p == Long.class)) out[i] = ((Integer) out[i]).longValue();
        }
        return out;
    }
}
