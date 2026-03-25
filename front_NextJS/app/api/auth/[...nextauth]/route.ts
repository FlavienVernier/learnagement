import NextAuth, {User} from "next-auth"

import Credentials from "next-auth/providers/credentials"
import axios from "axios";

//import SetCookie from "@/app/connection/setCookie"

const handler= NextAuth({
    providers: [
        Credentials({

            // You can specify which fields should be submitted, by adding keys to the `credentials` object.
            // e.g. domain, username, password, 2FA token, etc.
            credentials: {
                username: {label: "username", type: "text"},
                password: {label: "password", type: "password"},
            },
            authorize: async (credentials): Promise<User | null> => {
                if (!credentials) return null

                // let formData = new FormData()
                // formData.append("username", credentials.username)
                // formData.append("password", credentials.password)

                // OAuth2PasswordRequestForm attend du x-www-form-urlencoded
                const params = new URLSearchParams()
                params.append("username", credentials.username)
                params.append("password", credentials.password)

                try {
                    //const res = await axios.post("http://learnagement_phpbackend_dev/connection/authenticate.php", formData, {withCredentials: true})
                    //const res = await axios.post(process.env.PHP_BACKEND_DOCKER_URL+"/connection/authenticate.php", formData, {withCredentials: true})
                    const res = await axios.post(
                        process.env.PYTHON_BACKEND_DOCKER_URL + ":" + process.env.PYTHON_BACKEND_DOCKER_PORT + "/token",
                        params,
                        { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
                    )

                    if (res.status === 200) {
                        // const sessionId = res.data['sessionId']
                        // await SetCookie(sessionId)
                        // return res.data['user'] as User
                        const { access_token } = res.data

                        // Décoder le payload JWT pour récupérer les infos user
                        const payload = JSON.parse(
                            Buffer.from(access_token.split(".")[1], "base64").toString()
                        )

                        return {
                            id:               payload.id,
                            email:            payload.email,
                            name:             `${payload.firstname} ${payload.lastname}`,
                            firstname:        payload.firstname,
                            lastname:         payload.lastname,
                            roles:            payload.roles,
                            password2update:  payload.password2update,
                            accessToken:      access_token,
                        } as User

                    } else {
                        return null
                    }
                } catch (err) {
                    console.error("Authentication failed", err)
                    return null
                }
            }
        }),
    ],
    callbacks: {
        async jwt({ token, user }) {
            // `user` est défini uniquement à la connexion
            if (user) {
                token.user = user
                token.accessToken = (user as any).accessToken
            }
            return token
        },

        async session({ session, token }) {
            // Injecte l'utilisateur dans la session
            session.user = token.user as User
            session.accessToken = token.accessToken as string
            return session
        },

        async redirect({ url, baseUrl }) {

            // Rediriger vers une page spécifique après la connexion
            return '/homepage';
        }
    },
    pages: {
        signIn: "/connection", // page de connexion par défaut
    },
    //secret: process.env.INSTANCE_SECRET
    secret: process.env.NEXTAUTH_SECRET
})

export {handler as GET, handler as POST}