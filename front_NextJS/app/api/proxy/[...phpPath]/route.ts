// app/api/proxy/[...phpPath]/route.ts
// ToDo rename phpPath to apiPath
import axios from "axios";
import { NextRequest } from "next/server";
import { getServerSession } from "next-auth";

export async function POST(req: NextRequest) {
    return handleRequest(req, 'POST');
}

export async function GET(req: NextRequest) {
    return handleRequest(req, 'GET');
}

export async function handleRequest(req: NextRequest, method: string) {
    // Récupère l'url du backend php
    //const phpurl = process.env.PHP_BACKEND_DOCKER_URL;
    const pythonUrl = process.env.PYTHON_BACKEND_DOCKER_URL;
    const pythonPort = process.env.PYTHON_BACKEND_DOCKER_PORT;
    // Récupère tout ce qu’il y a après /api/proxy/
    const fullPath = req.nextUrl.pathname.replace(/^\/api\/proxy\//, "");
    // Query params (ex: /api/proxy/users?page=1 → ?page=1)
    const queryString = req.nextUrl.search ?? "";
    // Récupère le type de content utilisé
    //const contentType = req.headers.get("content-type") || "application/x-www-form-urlencoded";
    const contentType = req.headers.get("content-type") || "application/json";
    // Récupère le corps tel quel
    const body = method === 'POST' ? await req.text() : undefined; // pas de body pour GET

    // Récupère le JWT depuis la session NextAuth
    const session = await getServerSession() as any;
    const accessToken = session?.accessToken;

    try {
        const cookie = req.headers.get("cookie") || "";

        const response = await axios({
            method: method,
	        //url: `${phpurl}/${fullPath}.php`,
            //url: `http://learnagement_phpbackend_dev/${fullPath}.php`, // 'php' correspond au nom docker du container php
            url: `${pythonUrl}:${pythonPort}/${fullPath}${queryString}`,
            data: body,
            headers: {
                "Content-Type": contentType,
                ...(accessToken && { "Authorization": `Bearer ${accessToken}` }),
                //Cookie: cookie
            },
            //withCredentials: true,
        })

        return new Response(JSON.stringify(response.data), {
            status: response.status,
            headers: {
                "Content-Type": "application/json",
            },
        });

    } catch (error: any) {
        const status  = error.response?.status  ?? 500;
        const detail  = error.response?.data    ?? error.message;

        console.error("Erreur proxy:", `${pythonUrl}:${pythonPort}/${fullPath}${queryString}`);
        console.error("Erreur proxy:", detail);

        return new Response(JSON.stringify({ error: detail }), { status });
        /*return new Response(JSON.stringify({ error: "Erreur dans le proxy." + phpurl}), {
            status: 500,
        });*/
    }
}
