/**
 * Login Page — /login
 * Role-based authentication (Admin, Doctor, Nurse)
 */
export default function LoginPage() {
    return (
        <main className="flex min-h-screen items-center justify-center">
            <div className="rounded-xl bg-slate-800 p-8 shadow-xl">
                <h1 className="mb-6 text-2xl font-bold">Sign In</h1>
                {/* TODO: Implement login form with NextAuth.js */}
                <p className="text-slate-400">Authentication coming soon...</p>
            </div>
        </main>
    );
}
