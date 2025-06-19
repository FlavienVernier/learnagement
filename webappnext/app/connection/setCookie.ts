'use server'

import { cookies } from 'next/headers'

export default async function create(sessionId: string) {
    const cookieStore = await cookies()

    cookieStore.set({
        name: 'PHPSESSID',
        value: sessionId,
        httpOnly: true,
        path: '/',
    })
}