'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import Layout from '../../components/Layout';

export default function Resume() {
  const [windowWidth, setWindowWidth] = useState(0);

  useEffect(() => {
    // Set initial window width
    setWindowWidth(window.innerWidth);

    // Handle window resize
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    window.addEventListener('resize', handleResize);

    // Animate intro tile first
    const introTile = document.querySelector('.tile.intro');
    if (introTile) {
      setTimeout(() => {
        introTile.classList.add('animate');
      }, 300);
    }

    // Animate PDF button
    const pdfButtons = document.querySelectorAll('.resumePDF') as NodeListOf<HTMLElement>;
    if (pdfButtons.length > 1) {
      // Target the second button (PDF button)
      setTimeout(() => {
        pdfButtons[1].style.opacity = '1';
        pdfButtons[1].style.transform = 'translateY(0)';
      }, 600);
    }

    // Animate resume parts (matching original timing)
    const resumeParts = document.querySelectorAll('.resume-part');
    resumeParts.forEach((part, index) => {
      setTimeout(() => {
        part.classList.add('animate');
      }, (index + 2) * 300); // Offset by 2 to account for intro tile and PDF button
    });

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Responsive styles based on window width
  const isMobile = windowWidth < 768;
  const isTablet = windowWidth >= 768 && windowWidth < 1200;
  const isDesktop = windowWidth >= 1200;

  const containerStyle = {
    display: 'flex',
    flexDirection: isMobile ? 'column' as const : 'row' as const,
    gap: isMobile ? '20px' : isTablet ? '30px' : '40px',
    padding: isMobile ? '20px' : isTablet ? '30px' : '40px',
    maxWidth: isDesktop ? '1400px' : 'none',
    margin: isDesktop ? '0 auto' : '0',
  };

  const sidebarStyle = {
    width: isMobile ? '100%' : isTablet ? '35%' : '35%',
    minWidth: isMobile ? 'auto' : isTablet ? '300px' : '350px',
    maxWidth: isDesktop ? '400px' : 'none',
    flexShrink: 0,
    order: isMobile ? 1 : 0,
  };

  const introTileStyle = {
    height: 'auto',
    minHeight: isMobile ? '320px' : isTablet ? '400px' : '500px',
    display: 'flex',
    flexDirection: 'column' as const,
    justifyContent: 'flex-start',
    alignItems: isMobile ? 'center' : 'flex-start',
    boxSizing: 'border-box' as const,
    overflow: 'hidden',
    backgroundColor: 'var(--tile-color)',
    borderRadius: '20px',
    padding: isMobile ? '30px' : '50px',
    transition: 'background-color 1s ease, opacity 1s ease-in, transform 0.1s ease-in',
    textAlign: isMobile ? 'center' as const : 'left' as const,
  };

  const selfieStyle = {
    width: isMobile ? '80px' : isTablet ? '100px' : '120px',
    height: isMobile ? '80px' : isTablet ? '100px' : '120px',
    borderRadius: '100%',
    objectFit: 'contain' as const,
  };

  const nameStyle = {
    fontSize: isMobile ? '24px' : '28px',
    margin: isMobile ? '15px 0 10px 0' : '20px 0 10px 0',
  };

  const titleStyle = {
    fontSize: isMobile ? '16px' : '18px',
    margin: isMobile ? '0 0 15px 0' : '0 0 20px 0',
  };

  const resumeSectionStyle = {
    width: isMobile ? '100%' : isTablet ? '65%' : '65%',
    padding: 0,
    flex: 1,
    overflowX: 'hidden' as const,
    order: isMobile ? 2 : 0,
  };

  const buttonStyle = {
    opacity: '0',
    transform: 'translateY(20px)',
    transition: 'opacity 2s ease-in, transform 0.3s ease-in',
    marginBottom: '25px',
    display: 'block',
    fontSize: isMobile ? '14px' : '16px',
    padding: isMobile ? '12px 16px' : '15px 20px',
    textAlign: 'center' as const,
  };

  const contactButtonStyle = {
    opacity: '100',
    transform: 'translateY(10px)',
    transition: 'opacity 2s ease-in, transform 0.3s ease-in',
    marginBottom: '25px',
    display: 'block',
    fontSize: isMobile ? '14px' : '16px',
    padding: isMobile ? '12px 16px' : '15px 20px',
    textAlign: 'center' as const,
  };

  const skillsListStyle = {
    color: 'var(--third-color)',
    display: 'grid',
    gridTemplateColumns: isMobile ? 'repeat(2, 1fr)' : isTablet ? 'repeat(3, 1fr)' : 'repeat(4, 1fr)',
    gap: isMobile ? '10px' : isTablet ? '12px' : '15px',
  };

  const skillItemStyle = {
    marginTop: '5px',
    marginBottom: '5px',
    fontSize: isMobile ? '12px' : isTablet ? '14px' : '16px',
  };

  const descriptionStyle = {
    fontSize: isMobile ? '14px' : isTablet ? '15px' : '16px',
    lineHeight: '1.6',
    marginBottom: isMobile ? '20px' : '40px',
  };

  const sectionHeadingStyle = {
    fontSize: isMobile ? '20px' : '24px',
    marginBottom: isMobile ? '15px' : '20px',
  };

  const jobTitleStyle = {
    fontSize: isMobile ? '16px' : isTablet ? '18px' : '20px',
    lineHeight: isMobile ? '1.3' : '1.4',
    color: 'var(--second-color)',
    marginBottom: '5px',
  };

  const jobDateStyle = {
    marginTop: '0px',
    fontSize: isMobile ? '14px' : '16px',
    marginBottom: isMobile ? '8px' : '10px',
    color: 'var(--third-color)',
  };

  const experienceItemStyle = {
    marginBottom: isMobile ? '25px' : '30px',
  };

  return (
    <Layout>
      <div className="container" style={containerStyle}>
        <section className="resume-sidebar" style={sidebarStyle}>
          <div className="tile intro" style={introTileStyle}>
            <Image src="/selfie.png" alt="Selfie" className="selfie" style={selfieStyle} width={120} height={120} unoptimized />
            <h1 style={nameStyle}>Ahmed Khafaji</h1>
            <h3 style={titleStyle}>Founder & Lead Engineer</h3>
            <p className="email" style={{ marginBottom: '-0.5rem' }}>ahmedkhafaji11@gmail.com</p>
            <p style={{ fontSize: '14px', color: '#666' }}>647-765-6229 | Toronto, Canada</p>
            <button
              onClick={() => window.location.href = 'mailto:ahmedkhafaji11@gmail.com'}
              className="button navbar-item contact-me resumePDF"
              style={contactButtonStyle}
            >
              Contact me
            </button>
          </div>
        </section>

        <section className="resume-section" style={resumeSectionStyle}>
          <button
            className="button navbar-item contact-me resumePDF"
            onClick={() => window.open('/resume.pdf')}
            style={buttonStyle}
          >
            Resume PDF📃
          </button>
          <div className="resume">
            <div className="resume-part small-intro">
              <h1 className="resume-part little-about-me" style={sectionHeadingStyle}>A little about me</h1>
              <p className="resume-part small-intro-description description" style={descriptionStyle}>
                I&apos;m a Software Engineering student at York University (GPA: 7.4/9) and founder of CAYDE SERVICES INC., a Canadian software company delivering government and campus-scale solutions. I&apos;ve bootstrapped and led development of scalable applications including yuMeet (55k+ users), enterprise billing systems, and government platforms, with expertise in React, Next.js, Node.js, PostgreSQL, and modern DevOps practices.
              </p>
            </div>
            
            <div className="resume-part experience">
              <h1 style={sectionHeadingStyle}>Experience</h1>
              <div className="resume-part experience-list" style={experienceItemStyle}>
                <h1 className="job-title" style={jobTitleStyle}>Founder & Lead Engineer @ CAYDE SERVICES INC.</h1>
                <h4 style={jobDateStyle}>2022 - Present</h4>
                <p className="description" style={descriptionStyle}>Bootstrapped and led a Canadian software company delivering government and campus-scale solutions. Built and scaled yuMeet, a university social platform with real-time messaging and event matchmaking. Oversaw technical architecture, hiring, partnerships, and go-to-market strategy.</p>
              </div>
              <div className="resume-part experience-list" style={experienceItemStyle}>
                <h1 className="job-title" style={jobTitleStyle}>Senior Full-Stack Developer @ Wood Manufacturer</h1>
                <h4 style={jobDateStyle}>Feb 2024 - Present</h4>
                <p className="description" style={descriptionStyle}>Led a team of 5 developers in refactoring an internal system using PHP and JavaScript, improving performance by 40%. Architected and optimized database structures, reducing query times by 30%. Enhanced system security and mentored junior developers.</p>
              </div>
              <div className="resume-part experience-list" style={experienceItemStyle}>
                <h1 className="job-title" style={jobTitleStyle}>Senior Full-Stack Developer & Team Lead @ Lightring AI</h1>
                <h4 style={jobDateStyle}>Nov 2022 - Present</h4>
                <p className="description" style={descriptionStyle}>Directed development of critical projects for government and healthcare sectors, increasing client retention by 15%. Introduced CI/CD pipelines and DevOps practices, reducing deployment times by 50%. Led multi-platform app development boosting workflow efficiency by 25%.</p>
              </div>
            </div>

            <div className="resume-part projects" style={{ marginTop: '20px' }}>
              <h1 style={sectionHeadingStyle}>Key Projects</h1>
              <div className="resume-part projects-list" style={experienceItemStyle}>
                <h1 className="job-title" style={jobTitleStyle}>yuMeet - Campus Social App</h1>
                <h4 style={jobDateStyle}>2022 - Present</h4>
                <p className="description" style={descriptionStyle}>Led development of a scalable matchmaking and messaging platform for York University students, supporting 55k+ users with real-time messaging, user verification, and personalized recommendations.</p>
              </div>
              <div className="resume-part projects-list" style={experienceItemStyle}>
                <h1 className="job-title" style={jobTitleStyle}>Enterprise Billing System</h1>
                <h4 style={jobDateStyle}>2024</h4>
                <p className="description" style={descriptionStyle}>Architected and developed a scalable billing system for the Iraq government, processing over 100k daily transactions with microservices architecture ensuring 99.9% uptime.</p>
              </div>
              <div className="resume-part projects-list" style={experienceItemStyle}>
                <h1 className="job-title" style={jobTitleStyle}>Government E-Visa Platform</h1>
                <h4 style={jobDateStyle}>2023</h4>
                <p className="description" style={descriptionStyle}>Built comprehensive visa application system for Iraq ministry, reducing application processing time by 40% and engaging 50k+ monthly users.</p>
              </div>
              <div className="resume-part projects-list" style={experienceItemStyle}>
                <h1 className="job-title" style={jobTitleStyle}>Real-Time E-Commerce Auction Platform</h1>
                <h4 style={jobDateStyle}>2023</h4>
                <p className="description" style={descriptionStyle}>Built secure, scalable auction system with real-time bidding, attracting 10k+ active users in first month and protecting over $500k in transactions.</p>
              </div>
            </div>
            
            <div className="resume-part education" style={{ marginBottom: '3rem' }}>
              <h1 style={sectionHeadingStyle}>Education</h1>
              <div className="resume-part education-list">
                <h1 style={jobTitleStyle}>York University</h1>
                <h2 style={{ color: 'var(--third-color)', marginTop: '5px', marginBottom: '5px' }}>Bachelor of Engineering - Software Engineering</h2>
              </div>
            </div>
            
            <div className="resume-part skills">
              <h1 style={sectionHeadingStyle}>Skills</h1>
              <div className="resume-part skills-list" style={skillsListStyle}>
                <h1 style={skillItemStyle}>Python</h1>
                <h1 style={skillItemStyle}>JavaScript</h1>
                <h1 style={skillItemStyle}>TypeScript</h1>
                <h1 style={skillItemStyle}>Java</h1>
                <h1 style={skillItemStyle}>C</h1>
                <h1 style={skillItemStyle}>PHP</h1>
                <h1 style={skillItemStyle}>React</h1>
                <h1 style={skillItemStyle}>Next.js</h1>
                <h1 style={skillItemStyle}>Node.js</h1>
                <h1 style={skillItemStyle}>Express</h1>
                <h1 style={skillItemStyle}>PostgreSQL</h1>
                <h1 style={skillItemStyle}>MongoDB</h1>
                <h1 style={skillItemStyle}>Redis</h1>
                <h1 style={skillItemStyle}>Docker</h1>
                <h1 style={skillItemStyle}>Kubernetes</h1>
                <h1 style={skillItemStyle}>Jenkins</h1>
              </div>
            </div>
          </div>
        </section>
      </div>
    </Layout>
  );
}