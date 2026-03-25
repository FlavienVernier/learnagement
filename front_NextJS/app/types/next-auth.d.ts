// types/next-auth.d.ts
import NextAuth from "next-auth"

declare module "next-auth" {
    interface User {
        id: string;
        email: string;
        firstname: string;
        lastname: string;
        roles: string[];
        password2update: boolean;
        accessToken: string;
    }
    interface Session {
        user: User
        accessToken: string
        /*user: {
            id: string;
            email: string;
            firstname: string;
            lastname: string;
        }*/
    }
}

declare module "next-auth/jwt" {
    interface JWT {
        user: import("next-auth").User
        accessToken: string
        /*user: {
            id: string;
            email: string;
            firstname: string;
            lastname: string;
        }*/
    }
}
