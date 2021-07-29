export const HomePage = () => {
  return (
    <div>
      <h2>STX Project starter</h2>
      <p>This App is created in order to support kickoff phase of new projects</p>
      <p>
        It provides a default set of features that are very likely to be used across most of the new
        projects in STX along with a common, fresh & stable architecture & implemented
        best-practices.
      </p>
      <h3>Backend features:</h3>
      <ul>
        <li>Django setup</li>
        <li>Authorization module along with login, registration & password reset</li>
        <li>Email setup</li>
        <li>Celery setup</li>
        <li>File upload (TODO: WIP)</li>
        <li>Test coverage (TODO: WIP)</li>
      </ul>
      <h3>Devops features</h3>
      <ul>
        <li>Local env setup with docker-compose</li>
        <li>Local app wiring through nginx</li>
        <li>Configurable AWS CI (TODO: WIP)</li>
        <li>CD through AWS CodePipeline</li>
        <li>Staging AWS architecture deployment with terraform & plugin system</li>
      </ul>
      <h3>Frontend features</h3>
      <ul>
        <li>CRA React setup with TypeScript</li>
        <li>Wiring with Redux using best practices (Redux Toolkit)</li>
        <li>Support for redux-saga</li>
        <li>Support for styled components</li>
        <li>Lazy loading</li>
        <li>i18n support</li>
        <li>Connection with backend</li>
        <li>Forms & validation setup using Formik & yup</li>
      </ul>
      <h3>Testing features</h3>
      <ul>
        <li>E2E testing env using Cypress</li>
        <li>Linting & code-formatting using pre-commit, black and prettier</li>
      </ul>
    </div>
  );
};
