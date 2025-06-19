// types/next-auth.d.ts
import NextAuth from "next-auth"

declare module "next-auth" {
    interface Session {
        user: {
            id: string;
            email: string;
            firstname: string;
            lastname: string;
        }
    }

    interface User {
        id: string;
        email: string;
        firstname: string;
        lastname: string;
    }
}

declare module "next-auth/jwt" {
    interface JWT {
        user: {
            id: string;
            email: string;
            firstname: string;
            lastname: string;
        }
    }
}
