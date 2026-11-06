import { withAuth } from "next-auth/middleware"

export default withAuth({
    pages: {
        signIn: "/connection",
    },
})

export const config = {
    matcher: [
        //"/homepage:path*",
        //"/modules:path*",
        // Protège tout sauf : health, api, assets Next, favicon et fichiers statiques (avec extension)
        "/((?!health|_next/static|_next/image|favicon.ico).*)"
    ],
}
