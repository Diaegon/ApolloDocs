export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  success: boolean;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface UserPublic {
  id: number;
  username: string;
  email: string;
}

export interface AuthError {
  message: string;
  status?: number;
}
