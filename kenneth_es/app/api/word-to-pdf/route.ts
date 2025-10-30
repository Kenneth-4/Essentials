import { NextResponse } from 'next/server';
import { convertWordToPdf } from '@/lib/converters/wordToPdf';

export async function POST(req: Request) {
  const formData = await req.formData();
  const file = formData.get('file') as File;
  const pdfBuffer = await convertWordToPdf(file);
  return new NextResponse(pdfBuffer, {
    headers: { 'Content-Type': 'application/pdf' },
  });
}
