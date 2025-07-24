import { mount } from 'svelte';
import './app.css';
import App from './App.svelte';
import { client } from './client/client.gen';

const app = mount(App, {
  target: document.getElementById('app')!,
});

client.setConfig({ baseUrl: import.meta.env.VITE_API_URL });

export default app;
