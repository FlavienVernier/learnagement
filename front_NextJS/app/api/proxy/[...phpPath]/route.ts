// app/api/proxy/[...phpPath]/route.ts
import axios from "axios";
import { NextRequest } from "next/server";
import { getToken } from "next-auth/jwt";

export async function POST(req: NextRequest) {
    return handleRequest(req, 'POST');
}

export async function GET(req: NextRequest) {
    return handleRequest(req, 'GET');
}

export async function handleRequest(req: NextRequest, method: string) {
    // Récupère l'url du backend php
    //const phpurl = process.env.PHP_BACKEND_DOCKER_URL;
    const backendUrl =
                    process.env.INSTANCE_PROTOCOL + "://" +
                    process.env.BACKEND_PYTHON_DOCKER_URL + ":" +
                    process.env.BACKEND_PYTHON_DOCKER_PORT //+ "/token"
    // Récupère tout ce qu’il y a après /api/proxy/
    const fullPath = req.nextUrl.pathname.replace(/^\/api\/proxy\//, "");
    // Récupère le type de content utilisé
    const contentType = req.headers.get("content-type") || "application/x-www-form-urlencoded";
    // Récupère le corps tel quel
    const body = method === 'POST' ? await req.text() : undefined; // pas de body pour GET

    // Récupère le JWT du backend stocké dans la session NextAuth
    const token = await getToken({ req, secret: process.env.INSTANCE_SECRET });
    const backendJwt = (token?.user as any)?.jwt_token;

    const headers: Record<string, string> = {
        "Content-Type": contentType,
    };
    if (backendJwt) {
        headers.Authorization = `Bearer ${backendJwt}`;
    }

    try {
        const response = await axios({
            method: method,
	        url: `${backendUrl}/${fullPath}${req.nextUrl.search}`,
            data: body,
            headers: {
                "Content-Type": contentType,
                Authorization: `Bearer ${backendJwt}`,
            },
        })

        return new Response(JSON.stringify(response.data), {
            status: response.status,
            headers: {
                "Content-Type": "application/json",
            },
        });

    } catch (error: any) {
        console.error("Erreur proxy:", error.message);
        // Renvoie le vrai statut du backend (401, 403, 404...) au lieu d'un 500 systématique
        const status = error.response?.status ?? 500;
        return new Response(
            JSON.stringify(error.response?.data ?? { error: "Erreur dans le proxy." }),
            { status, headers: { "Content-Type": "application/json" } }
        );
    }
}
