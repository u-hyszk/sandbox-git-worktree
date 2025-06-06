import { AdCopyGenerationRequest, AdCopyGenerationResponse, ErrorResponse } from '@/types/api'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      let errorData: ErrorResponse
      try {
        errorData = await response.json()
      } catch {
        throw new ApiError(
          `HTTP ${response.status}: ${response.statusText}`,
          response.status
        )
      }
      
      throw new ApiError(
        errorData.message || `HTTP ${response.status}: ${response.statusText}`,
        response.status,
        errorData.code
      )
    }

    return response.json()
  }

  async generateAdCopy(request: AdCopyGenerationRequest): Promise<AdCopyGenerationResponse> {
    const response = await fetch(`${this.baseUrl}/generate-ad-copy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    })

    return this.handleResponse<AdCopyGenerationResponse>(response)
  }
}

export const apiClient = new ApiClient()

export { ApiError }