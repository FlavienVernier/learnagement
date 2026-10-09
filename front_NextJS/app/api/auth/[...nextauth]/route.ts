import NextAuth, { User } from "next-auth"
import Credentials from "next-auth/providers/credentials"
import axios from "axios"
import { jwtDecode } from "jwt-decode"

const handler = NextAuth({
    providers: [
        Credentials({
            credentials: {
                username: { label: "username", type: "text" },
                password: { label: "password", type: "password" },
            },
            authorize: async (credentials): Promise<User | null> => {
                if (!credentials) return null

                const backendUrl =
                    process.env.INSTANCE_PROTOCOL + "://" +
                    process.env.BACKEND_PYTHON_DOCKER_URL + ":" +
                    process.env.BACKEND_PYTHON_DOCKER_PORT + "/token"

                const formData = new URLSearchParams()
                formData.append("username", credentials.username)
                formData.append("password", credentials.password)
                formData.append("grant_type", "password")

                let res
                try {
                    res = await axios.post(backendUrl, formData, {
                        headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    })
                } catch (err) {
                    // Erreur réseau/serveur (backend injoignable, 500, etc.)
                    // Symétrique au "Connection error" côté PHP/Dash
                    console.error("Connection error calling backend:", err instanceof Error ? err.message : err)
                    throw new Error("Connection error")
                }

                const responseData = res.data

                if (!responseData || !responseData.access_token) {
                    // Symétrique au message "Incorrect login or password." de login.php
                    console.error("Incorrect login or password for user:", credentials.username)
                    throw new Error("Incorrect login or password")
                }

                const jwt = responseData.access_token

                let decoded
                try {
                    decoded = jwtDecode<{
                        id: number
                        email: string
                        firstname: string
                        lastname: string
                        roles: string[]
                        exp: number
                        password2update: boolean
                    }>(jwt)
                } catch (err) {
                    // Symétrique au bloc catch "Token invalide" de login.php
                    console.error("Token invalide:", err instanceof Error ? err.message : err)
                    throw new Error("Invalid token")
                }

                if (decoded.exp < Math.floor(Date.now() / 1000)) {
                    // Symétrique à la vérification d'expiration de login.php
                    console.error("Token expiré pour l'utilisateur:", decoded.email)
                    throw new Error("Token expired")
                }

                console.log(`Utilisateur : ${decoded.email} ${decoded.firstname} ${decoded.lastname}`)
                console.log(`Expire à : ${new Date(decoded.exp * 1000).toISOString()}`)

                return {
                    id: String(decoded.id),
                    email: decoded.email,
                    name: `${decoded.firstname} ${decoded.lastname}`,
                    firstname: decoded.firstname,
                    lastname: decoded.lastname,
                    roles: decoded.roles,
                    jwt_token: jwt,
                } as User
            }
        }),
    ],
    callbacks: {
        async jwt({ token, user }) {
            if (user) {
                token.user = user
            }
            return token
        },

        async session({ session, token }) {
            session.user = token.user
            return session
        },

        async redirect({ url, baseUrl }) {
            return '/homepage';
        }
    },
    pages: {
        signIn: "/connection",
    },
    secret: process.env.INSTANCE_SECRET
})

export { handler as GET, handler as POST }