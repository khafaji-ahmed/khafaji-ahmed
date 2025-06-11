import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ahmed's Portfolio v2",
  description: "Ahmed Khafaji - Software Engineering Student & Founder",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" type="image/png" href="/favicon.png" />
        <style>{`
          link[rel="icon"] {
            border-radius: 50%;
          }
        `}</style>
      </head>
      <body>
        {children}
      </body>
    </html>
  );
}