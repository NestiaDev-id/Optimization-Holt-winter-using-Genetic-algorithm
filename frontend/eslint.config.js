import js from "@eslint/js";
import globals from "globals";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["dist"] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
    plugins: {
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "react-refresh/only-export-components": [
        "warn",
        { allowConstantExport: true },
      ],
      // Disable the unused-vars rule
      "no-unused-vars": "off", // Disable for all files, if you need more specific control, you can add for 'ts' and 'tsx' files

      // Disable React specific unused variable rules
      "react/jsx-uses-react": "off", // React 17 and above no longer require 'React' to be in scope
      "react/jsx-uses-vars": "off", // Disable unused variables for React components

      // You can also disable unused hooks check (if needed)
      "react-hooks/rules-of-hooks": "off",
      "react-hooks/exhaustive-deps": "off",
    },
  }
);
