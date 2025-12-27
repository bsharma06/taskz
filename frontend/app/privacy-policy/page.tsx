'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated, getStoredUser, clearAuth } from '@/lib/auth';
import { Sidebar } from '@/components/Sidebar';
import { MobileMenu } from '@/components/MobileMenu';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Clock, Bell, Power, Shield } from 'lucide-react';

export default function PrivacyPolicyPage() {
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/signin');
      return;
    }
  }, [router]);

  const handleLogout = () => {
    clearAuth();
    router.push('/signin');
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

  const user = getStoredUser();

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <MobileMenu />
      <div className="flex-1 flex flex-col overflow-hidden md:ml-64">
        {/* Top Header Bar */}
        <header className="border-b bg-card px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-semibold">Privacy Policy</h3>
              <p className="text-sm text-muted-foreground">
                {getGreeting()}, {user?.user_name || 'User'}!
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="icon" className="h-9 w-9">
                <Clock className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" className="h-9 w-9">
                <Bell className="h-5 w-5" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="h-9 w-9"
                onClick={handleLogout}
              >
                <Power className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-4xl mx-auto space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Privacy Policy
                </CardTitle>
                <CardDescription>
                  Last updated: {new Date().toLocaleDateString()}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <section>
                  <h3 className="text-lg font-semibold mb-3">1. Introduction</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    Welcome to Taskz. We are committed to protecting your personal information and your right to privacy.
                    This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you
                    use our task management application.
                  </p>
                </section>

                <section>
                  <h3 className="text-lg font-semibold mb-3">2. Information We Collect</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed mb-2">
                    We collect information that you provide directly to us, including:
                  </p>
                  <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1 ml-4">
                    <li>Name and email address when you create an account</li>
                    <li>Task information including titles, descriptions, due dates, and assignments</li>
                    <li>User preferences and settings</li>
                    <li>Any other information you choose to provide</li>
                  </ul>
                </section>

                <section>
                  <h3 className="text-lg font-semibold mb-3">3. How We Use Your Information</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed mb-2">
                    We use the information we collect to:
                  </p>
                  <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1 ml-4">
                    <li>Provide, maintain, and improve our services</li>
                    <li>Process and manage your tasks and assignments</li>
                    <li>Send you technical notices and support messages</li>
                    <li>Respond to your comments and questions</li>
                    <li>Monitor and analyze usage patterns and trends</li>
                  </ul>
                </section>

                <section>
                  <h3 className="text-lg font-semibold mb-3">4. Data Security</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    We implement appropriate technical and organizational security measures to protect your personal
                    information. This includes encryption of data in transit and at rest, secure authentication
                    mechanisms, and regular security assessments. However, no method of transmission over the Internet
                    or electronic storage is 100% secure, and we cannot guarantee absolute security.
                  </p>
                </section>

                <section>
                  <h3 className="text-lg font-semibold mb-3">5. Data Retention</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    We retain your personal information for as long as necessary to provide our services and fulfill
                    the purposes outlined in this Privacy Policy, unless a longer retention period is required or
                    permitted by law.
                  </p>
                </section>

                <section>
                  <h3 className="text-lg font-semibold mb-3">6. Your Rights</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed mb-2">
                    You have the right to:
                  </p>
                  <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1 ml-4">
                    <li>Access and receive a copy of your personal information</li>
                    <li>Rectify inaccurate or incomplete information</li>
                    <li>Request deletion of your personal information</li>
                    <li>Object to or restrict processing of your information</li>
                    <li>Data portability</li>
                  </ul>
                </section>

                <section>
                  <h3 className="text-lg font-semibold mb-3">7. Third-Party Services</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    Our application may contain links to third-party websites or services. We are not responsible for
                    the privacy practices of these third parties. We encourage you to review their privacy policies
                    before providing any personal information.
                  </p>
                </section>

                <section>
                  <h3 className="text-lg font-semibold mb-3">8. Changes to This Privacy Policy</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    We may update this Privacy Policy from time to time. We will notify you of any changes by posting
                    the new Privacy Policy on this page and updating the "Last updated" date. You are advised to review
                    this Privacy Policy periodically for any changes.
                  </p>
                </section>

                <section>
                  <h3 className="text-lg font-semibold mb-3">9. Contact Us</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    If you have any questions about this Privacy Policy or our data practices, please contact us through
                    the Support page or by email at support@taskz.com.
                  </p>
                </section>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </div>
  );
}

