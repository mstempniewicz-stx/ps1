export interface User {
  id: string;
}

export interface SignUpData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
}

interface LoginData {
  email: string;
  password: string;
}
