
import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
  thresholds: { http_req_duration: ['p(95)<300'] }
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/health`);
  check(res, { 'status 200': r => r.status === 200 });
  sleep(1);
}
