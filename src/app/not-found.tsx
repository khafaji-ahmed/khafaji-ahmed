'use client';

import { useEffect } from 'react';
import Layout from '../components/Layout';
import Link from 'next/link';

export default function NotFound() {
  useEffect(() => {
    // Animate the 404 content with the same pattern as other pages
    const animateElements = () => {
      const elements = document.querySelectorAll('.not-found-content > *');
      elements.forEach((element, index) => {
        setTimeout(() => {
          element.classList.add('animate');
        }, index * 300);
      });
    };

    setTimeout(animateElements, 200);
  }, []);

  return (
    <Layout>
      <section className="not-found-section">
        <div className="not-found-content">
          <div className="not-found-number">404</div>
          <h1 className="not-found-title">Page Not Found</h1>
          <p className="not-found-description">
            Oops! The page you&apos;re looking for doesn&apos;t exist. 
            It might have been moved, deleted, or you entered the wrong URL.
          </p>
          <div className="not-found-actions">
            <Link href="/" className="button primary-button">
              Go Home
            </Link>
            <Link href="/about" className="button secondary-button">
              About Me
            </Link>
          </div>
        </div>
      </section>
      
      <style jsx>{`
        .not-found-section {
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 70vh;
          padding: 2rem;
        }

        .not-found-content {
          text-align: center;
          max-width: 600px;
        }

        .not-found-content > * {
          opacity: 0;
          transform: translateY(30px);
          transition: all 0.6s ease-out;
        }

        .not-found-content > *.animate {
          opacity: 1;
          transform: translateY(0);
        }

        .not-found-number {
          font-size: clamp(8rem, 15vw, 12rem);
          font-weight: 900;
          color: #f5a623;
          line-height: 1;
          margin-bottom: 1rem;
          text-shadow: 0 4px 8px rgba(245, 166, 35, 0.3);
        }

        .not-found-title {
          font-size: clamp(2rem, 5vw, 3rem);
          font-weight: 700;
          color: #ffffff;
          margin-bottom: 1.5rem;
          line-height: 1.2;
        }

        .not-found-description {
          font-size: 1.125rem;
          color: #c7c8c8;
          line-height: 1.6;
          margin-bottom: 2.5rem;
          max-width: 500px;
          margin-left: auto;
          margin-right: auto;
        }

        .not-found-actions {
          display: flex;
          gap: 1rem;
          justify-content: center;
          flex-wrap: wrap;
        }

        .button {
          padding: 12px 24px;
          border-radius: 8px;
          font-weight: 600;
          text-decoration: none;
          transition: all 0.3s ease;
          border: 2px solid transparent;
          cursor: pointer;
          font-size: 1rem;
          min-width: 140px;
        }

        .primary-button {
          background-color: #f5a623;
          color: #1a1a1a;
          border-color: #f5a623;
        }

        .primary-button:hover {
          background-color: #e6951f;
          border-color: #e6951f;
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(245, 166, 35, 0.3);
        }

        .secondary-button {
          background-color: transparent;
          color: #c7c8c8;
          border-color: #c7c8c8;
        }

        .secondary-button:hover {
          background-color: #c7c8c8;
          color: #1a1a1a;
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(199, 200, 200, 0.2);
        }

        @media (max-width: 768px) {
          .not-found-section {
            min-height: 60vh;
            padding: 1rem;
          }

          .not-found-actions {
            flex-direction: column;
            align-items: center;
          }

          .button {
            width: 200px;
          }
        }

        @media (max-width: 480px) {
          .not-found-description {
            font-size: 1rem;
          }
        }
      `}</style>
    </Layout>
  );
}