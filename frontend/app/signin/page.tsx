'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authApi } from '@/lib/api';
import { setStoredToken, setStoredUser } from '@/lib/auth';

export default function SignInPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authApi.login(email, password);
      
      // Check if response has access_token
      if (!response || !response.access_token) {
        throw new Error('Invalid response from server');
      }
      
      setStoredToken(response.access_token);
      
      // Get user info - make this optional, don't block login if it fails
      try {
        const user = await authApi.getCurrentUser();
        if (user) {
          setStoredUser(user);
        }
      } catch (userError: any) {
        console.error('Failed to get user info:', userError);
        // Continue anyway - token is set, user can still proceed
      }
      
      router.push('/dashboard');
    } catch (err: any) {
      console.error('Login error:', err);
      console.error('Error details:', {
        message: err.message,
        code: err.code,
        response: err.response,
        stack: err.stack
      });
      
      if (err.code === 'ERR_NETWORK' || err.message === 'Network Error' || err.message?.includes('Network')) {
        setError('Network error. Please make sure the backend server is running on http://localhost:8000');
      } else if (err.response?.status === 401) {
        setError('Invalid email or password');
      } else {
        setError(err.response?.data?.detail || err.message || 'Login failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-2 text-center text-4xl font-semibold text-foreground">
            Sign in to Taskz
          </h2>
          <p className="mt-4 text-center text-sm text-muted-foreground">
            Or{' '}
            <Link href="/signup" className="font-medium text-primary hover:text-primary/80">
              create a new account
            </Link>
          </p>
        </div>
        <form className="mt-8 space-y-8" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-destructive/10 border border-destructive/20 p-4">
              <div className="text-sm text-destructive">{error}</div>
            </div>
          )}
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email" className="sr-only">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-3 border border-input bg-background placeholder-muted-foreground text-foreground rounded-t-md focus:outline-none focus:ring-0 focus:ring-ring focus:border-ring focus:z-10 sm:text-sm"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-3 border border-input bg-background placeholder-muted-foreground text-foreground rounded-b-md focus:outline-none focus:ring-0 focus:ring-ring focus:border-ring focus:z-10 sm:text-sm"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-lg font-medium rounded-md text-secondary-foreground bg-secondary hover:bg-secondary/90 focus:outline-none focus:ring-0 focus:ring-offset-1 focus:ring-ring disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

