import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10, // 10 utilisateurs virtuels
  duration: '30s', // Test de 30 secondes

  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% des requêtes < 500ms
    http_req_failed: ['rate<0.1'], // Moins de 10% d'échecs
  },
};

export default function () {
  // Test de la page d'accueil
  let response = http.get('http://localhost:8000/');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1); // Pause de 1 seconde entre les requêtes
}