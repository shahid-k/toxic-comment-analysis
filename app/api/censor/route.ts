import { NextResponse } from 'next/server'
import axios from 'axios'

export async function POST(request: Request) {
  try {
    const { text } = await request.json()

    const response = await axios.post(
      'https://1vctzd9dac.execute-api.us-east-1.amazonaws.com/api/text',
      {
        path: '/text',
        httpMethod: 'POST',
        body: JSON.stringify({ text }),
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )

    const result = JSON.parse(response.data.body)
    console.log(result)
    return NextResponse.json(result)
  } catch (error) {
    console.error('Error calling censorship API:', error)
    return NextResponse.json({ message: 'Internal Server Error' }, { status: 500 })
  }
}

