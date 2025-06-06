export interface AdCopyGenerationRequest {
  productName: string
  targetAudience: string
  appealPoints: string[]
  tone?: 'formal' | 'casual' | 'humorous' | 'professional' | 'friendly'
  numCopies?: number
}

export interface GeneratedAdCopy {
  copyText: string
  headline?: string
  callToAction?: string
  evaluation?: {
    relevanceScore?: number
    creativityScore?: number
    targetAudienceAppeal?: string
  }
}

export interface AdCopyGenerationResponse {
  generatedCopies: GeneratedAdCopy[]
}

export interface ErrorResponse {
  message: string
  code: string
}