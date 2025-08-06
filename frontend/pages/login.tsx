import { useState } from 'react';
import Image from 'next/image';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: implement authentication call
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <Image src="/volvo-logo.svg" alt="Volvo" width={120} height={120} />
      <form onSubmit={handleSubmit} className="mt-8 w-full max-w-sm space-y-4">
        <input
          className="border rounded w-full p-2"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          className="border rounded w-full p-2"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="w-full bg-blue-500 text-white rounded p-2" type="submit">
          Login
        </button>
      </form>
    </div>
  );
}
