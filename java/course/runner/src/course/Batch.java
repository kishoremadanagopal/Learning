package course;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

/**
 * Runs many jobs in one JVM for the course build's tests.
 * Usage: Batch <listFile> <resultFile>
 *   listFile: one job per line, "prefix|mode"
 *   resultFile: for each job, "@@JOB prefix" followed by everything the runner printed
 */
public final class Batch {
    public static void main(String[] args) throws Exception {
        ByteArrayOutputStream buf = new ByteArrayOutputStream();
        PrintStream cap = new PrintStream(buf, true, StandardCharsets.UTF_8);
        PrintStream console = System.out;
        System.setOut(cap);
        System.setErr(cap);
        StringBuilder results = new StringBuilder();
        List<String> jobs = Files.readAllLines(Paths.get(args[0]));
        int n = 0;
        for (String line : jobs) {
            if (line.isBlank()) continue;
            String[] p = line.split("\\|");
            buf.reset();
            try {
                Runner.run(p[0], "/tmp/course-batch", p[1], 10000);
            } catch (Throwable e) {
                cap.println("@@BATCH_ERROR " + e);
            }
            cap.flush();
            results.append("@@JOB ").append(p[0]).append('\n').append(buf.toString(StandardCharsets.UTF_8)).append('\n');
            if (++n % 25 == 0) console.println("  ran " + n + " / " + jobs.size());
        }
        Files.write(Paths.get(args[1]), results.toString().getBytes(StandardCharsets.UTF_8));
        console.println("  ran " + n + " jobs");
        System.exit(0);
    }
}
