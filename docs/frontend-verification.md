# Frontend verification

Run the frontend checks from the `frontend` directory:

```sh
npm run build
npm run lint
```

The build validates TypeScript and the production bundle. ESLint must report
no errors; the existing Fast Refresh warning in `main.tsx` is informational.
