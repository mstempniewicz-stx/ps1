module.exports = {
  defaultNamespace: 'translation',
  createOldCatalogs: false,
  locales: ['en'],
  output: 'src/lang/$LOCALE/$NAMESPACE.json',
  input: 'src/**/*.{js,ts,tsx}',
  sort: true,
};
