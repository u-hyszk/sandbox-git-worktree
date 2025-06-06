export * from './api'
import { GeneratedAdCopy } from './api'

export interface FormData {
  productName: string
  targetAudience: string
  appealPoints: string[]
  tone: 'formal' | 'casual' | 'humorous' | 'professional' | 'friendly'
  numCopies: number
}

export interface AppState {
  isLoading: boolean
  error: string | null
  results: GeneratedAdCopy[] | null
}