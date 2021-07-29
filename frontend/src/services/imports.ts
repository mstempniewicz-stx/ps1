export const namedImportToDefault = (
  promise: () => Promise<Record<string, React.ComponentType<any>>>,
  importName: string
) => async () => ({
  default: (await promise())[importName],
});
