import ConverterCard from "@/components/ConverterCard";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-6">
      <h1 className="text-3xl font-bold mb-8">File Converter</h1>
      <div className="grid md:grid-cols-3 gap-6">
        <ConverterCard title="Word to PDF" api="/api/word-to-pdf" />
        <ConverterCard title="PDF to Word" api="/api/pdf-to-word" />
        <ConverterCard title="YouTube to MP3" api="/api/youtube-to-mp3" />
      </div>
    </main>
  );
}