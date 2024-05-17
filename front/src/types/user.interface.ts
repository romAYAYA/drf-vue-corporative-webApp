export interface User {
  id?: number
  username: string

  first_name?: string
  last_name?: string
  email?: string
  password?: string
  profile: Profile
}

export interface Profile {
  bio: string
  avatar: string
}