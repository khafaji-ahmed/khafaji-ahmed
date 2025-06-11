'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [animatedElements, setAnimatedElements] = useState<string[]>([]);

  useEffect(() => {
    // Animate elements on page load
    const animateItems = (classNames: string[], delayMultiplier = 1) => {
      classNames.forEach((className, index) => {
        setTimeout(() => {
          setAnimatedElements(prev => [...prev, className]);
        }, index * 300 * delayMultiplier);
      });
    };

    // Reset animations
    setAnimatedElements([]);
    
    // Start animations
    setTimeout(() => {
      animateItems(['name'], 1);
      animateItems(['navbar-items'], 1);
      animateItems(['tiles'], 2);
    }, 100);
  }, []);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
    
    // Get nav and navlinks elements
    const nav = document.querySelector('.nav');
    const navlinks = document.querySelectorAll('.navlink');
    
    if (!isMenuOpen) {
      // Opening menu
      navlinks.forEach((link) => {
        (link as HTMLElement).style.display = 'block';
      });
      
      // Create GET IN TOUCH button for mobile menu
      const getInTouchButton = document.createElement('button');
      getInTouchButton.className = 'button navbar-item navlink';
      getInTouchButton.textContent = 'GET IN TOUCH';
      getInTouchButton.onclick = function () {
        window.location.href = 'mailto:ahmedkhafaji11@gmail.com';
      };
      nav?.appendChild(getInTouchButton);
    } else {
      // Closing menu
      navlinks.forEach((link) => {
        (link as HTMLElement).style.display = 'none';
      });
      
      // Remove existing GET IN TOUCH button
      const existingButton = document.querySelector('.button.navbar-item.navlink');
      if (existingButton) {
        existingButton.remove();
      }
    }
  };

  return (
    <div className="min-h-screen">
      <div className="wrapper">
        {/* Header Section */}
        <section className="header-section">
          <div className={`navbar ${isMenuOpen ? 'menu-open' : ''}`}>
            {/* Name */}
            <h1 className={`name ${animatedElements.includes('name') ? 'animate' : ''}`}>
              Ahmed
            </h1>

            {/* Desktop Navigation */}
            <div className={`nav`}>
              <div className={`navbar-item navlink ${animatedElements.includes('navbar-items') ? 'animate' : ''}`}>
                <Link href="/">Home</Link>
              </div>
              <div className={`navbar-item navlink ${animatedElements.includes('navbar-items') ? 'animate' : ''}`}>
                <Link href="/about">About</Link>
              </div>
              <div className={`navbar-item navlink ${animatedElements.includes('navbar-items') ? 'animate' : ''}`}>
                <Link href="/resume">Resume</Link>
              </div>
            </div>

            {/* Get in Touch Button (Desktop) */}
            <button
              onClick={() => window.location.href = 'mailto:ahmedkhafaji11@gmail.com'}
              className={`button navbar-item original-get-in-touch ${animatedElements.includes('navbar-items') ? 'animate' : ''}`}
            >
              GET IN TOUCH
            </button>

            {/* Mobile Menu Toggle */}
            <button
              onClick={toggleMenu}
              className="menu-toggle"
              aria-label="Toggle Menu"
            >
              <span className="hamburger"></span>
              <span className="hamburger"></span>
              <span className="hamburger"></span>
            </button>
          </div>
        </section>

        {/* Main Content */}
        {children}
      </div>
    </div>
  );
}