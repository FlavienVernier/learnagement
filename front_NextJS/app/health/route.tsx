export const dynamic = "force-dynamic"; // évite la mise en cache statique

export async function GET() {
    return Response.json({ status: "ok" });
}
