import { NextResponse } from 'next/server';

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const repoUrl = searchParams.get('repoUrl');
  const prompt = searchParams.get('prompt');
  
  if (!repoUrl || !prompt) {
    return NextResponse.json(
      { error: 'Missing repoUrl or prompt parameters' },
      { status: 400 }
    );
  }
  
  const apiUrl = process.env.BACKEND_API_URL || 'http://localhost:8000';
  
  try {
    const response = await fetch(`${apiUrl}/code`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ repoUrl, prompt }),
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    // Stream the response back to the frontend
    const stream = new ReadableStream({
      async start(controller) {
        const reader = response.body.getReader();
        
        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            controller.enqueue(value);
          }
        } finally {
          controller.close();
        }
      },
    });

    return new NextResponse(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  } catch (error) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
} 