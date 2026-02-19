import type { Metadata } from "next";
import "@/styles/globals.css";

export const metadata: Metadata = {
    title: "Drip-Sense Control Center",
    description: "Real-time IV drip monitoring dashboard",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en" className="dark">
            <body className="bg-slate-900 text-slate-50 font-sans">
                {/* TODO: Add sidebar layout, auth provider */}
                {children}
            </body>
        </html>
    );
}
