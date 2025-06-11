'use client';

import { useEffect } from 'react';
import Image from 'next/image';
import Layout from '../components/Layout';

export default function Home() {
  useEffect(() => {
    // Animate tiles exactly like the original JavaScript
    const tileElements = document.querySelectorAll('.tile');
    tileElements.forEach((tile, index) => {
      setTimeout(() => {
        tile.classList.add('animate');
      }, (index * 300) * 2); // delayMultiplier = 2 like original
    });
  }, []);

  const handleTileClick = (url: string) => {
    if (url.startsWith('http')) {
      window.open(url, '_blank');
    } else {
      window.location.href = url;
    }
  };

  return (
    <Layout>
      <section className="tiles-section">
        <div className="tiles">
          {/* About Tile - tile-2 (spans 2 columns) */}
          <div className="tile tile-2" onClick={() => handleTileClick('/about')}>
            <Image className="selfie-img" src="/selfie.png" alt="Selfie" width={120} height={120} unoptimized />
            <h1>Hey, I&apos;m Ahmed 👋🏻</h1>
            <svg
              className="right-arrow-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="60"
              height="60"
              fill="none"
            >
              <path
                stroke="#c7c8c8"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="3"
                d="M4.167 10h11.667M10.833 15l5-5M10.833 5l5 5"
              />
            </svg>
          </div>

          {/* Resume Tile */}
          <div className="tile resume" onClick={() => handleTileClick('/resume')}>
            <svg
              className="user-icon"
              width="40px"
              height="40px"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M5 21C5 17.134 8.13401 14 12 14C15.866 14 19 17.134 19 21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z"
                stroke="#f5a623"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <h1 className="resume-description">See my resume</h1>
            <svg
              className="right-arrow-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="60px"
              height="60px"
              fill="none"
            >
              <path
                stroke="#c7c8c8"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="3"
                d="M4.167 10h11.667M10.833 15l5-5M10.833 5l5 5"
              />
            </svg>
          </div>

          {/* GitHub Tile */}
          <div
            className="tile github"
            onClick={() => handleTileClick('https://github.com/khafaji-ahmed')}
          >
            <svg
              className="github-icon"
              width="40px"
              height="40px"
              viewBox="0 0 100 100"
              color='#f5a623ff'
              preserveAspectRatio="xMidYMid meet"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill="#f5a623ff"
                d="M48.854 0C21.839 0 0 22 0 49.217c0 21.756 13.993 40.172 33.405 46.69 2.427.49 3.316-1.059 3.316-2.362 0-1.141-.08-5.052-.08-9.127-13.59 2.934-16.42-5.867-16.42-5.867-2.184-5.704-5.42-7.17-5.42-7.17-4.448-3.015.324-3.015.324-3.015 4.934.326 7.523 5.052 7.523 5.052 4.367 7.496 11.404 5.378 14.235 4.074.404-3.178 1.699-5.378 3.074-6.6-10.839-1.141-22.243-5.378-22.243-24.283 0-5.378 1.94-9.778 5.014-13.2-.485-1.222-2.184-6.275.486-13.038 0 0 4.125-1.304 13.426 5.052a46.97 46.97 0 0 1 12.214-1.63c4.125 0 8.33.571 12.213 1.63 9.302-6.356 13.427-5.052 13.427-5.052 2.67 6.763.97 11.816.485 13.038 3.155 3.422 5.015 7.822 5.015 13.2 0 18.905-11.404 23.06-22.324 24.283 1.78 1.548 3.316 4.481 3.316 9.126 0 6.6-.08 11.897-.08 13.526 0 1.304.89 2.853 3.316 2.364 19.412-6.52 33.405-24.935 33.405-46.691C97.707 22 75.788 0 48.854 0z"
              />
            </svg>
            <h1 className="github-description">Look at my GitHub</h1>
            <svg
              className="right-arrow-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="60px"
              height="60px"
              fill="none"
            >
              <path
                stroke="#c7c8c8"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="3"
                d="M4.167 10h11.667M10.833 15l5-5M10.833 5l5 5"
              />
            </svg>
          </div>

          {/* Projects Tile */}
          <div className="tile projects">
            <h1 className="projects-description">Projects</h1>
            <p className="about-me-description">
              I have professional projects that I have worked on as lead developer available upon request.
              For personal projects, check out my github! ⌨️
            </p>
          </div>

          {/* Languages Tile - tile-3 (spans 3 columns) */}
          <div className="languages tile tile-3">
            <Image
              className="languages-img"
              src="/languages.png"
              alt="Languages"
              width={300}
              height={200}
              unoptimized
            />
            <h1 className="languages-description">Languages</h1>
            <svg
              className="right-arrow-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="60px"
              height="60px"
              fill="none"
            >
              <path
                stroke="#c7c8c8"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="3"
                d="M4.167 10h11.667M10.833 15l5-5M10.833 5l5 5"
              />
            </svg>
          </div>
        </div>
      </section>
    </Layout>
  );
}