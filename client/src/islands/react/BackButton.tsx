import React from 'react';
import { ArrowLeft } from 'lucide-react';

interface BackButtonProps {
  href: string;
  children?: React.ReactNode;
  className?: string;
}

export default function BackButton({ href, children = "Back", className = "" }: BackButtonProps) {
  return (
    <a 
      href={href}
      className={`inline-flex items-center gap-2 text-sm opacity-70 hover:opacity-100 transition-opacity ${className}`}
    >
      <ArrowLeft className="h-4 w-4" />
      {children}
    </a>
  );
}
