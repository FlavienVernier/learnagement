import { withAuth } from "next-auth/middleware"

export default withAuth({
    pages: {
        signIn: "/connection",
    },
})

export const config = {
    matcher: [
        "/homepage:path*",
        "/modules:path*"
    ],
}