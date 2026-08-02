import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
    base: "./",
    
    plugins: [react()],
    build: {
        outDir: path.resolve(__dirname, "../blocked-page-dist"),
        emptyOutDir: true,
        rollupOptions: {
            input: path.resolve(__dirname, "blocked.html"),
        },
    },
});