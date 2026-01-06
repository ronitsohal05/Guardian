/**
 * Geocoding service using OpenStreetMap Nominatim API
 */

export interface GeocodeResult {
  lat: number
  lng: number
  displayName?: string
}

/**
 * Convert address string to coordinates using Nominatim
 * @param address - Address string (e.g., "123 Main St, San Francisco, CA")
 * @returns GeocodeResult with lat/lng or throws error
 */
export async function geocodeAddress(address: string): Promise<GeocodeResult> {
  if (!address || address.trim().length === 0) {
    throw new Error('Address cannot be empty')
  }

  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`
    )

    if (!response.ok) {
      throw new Error('Geocoding service error')
    }

    const results = await response.json()

    if (!results || results.length === 0) {
      throw new Error(`Could not find coordinates for "${address}"`)
    }

    // Use first result
    const result = results[0]
    return {
      lat: parseFloat(result.lat),
      lng: parseFloat(result.lon), // Note: Nominatim uses 'lon' not 'lng'
      displayName: result.display_name,
    }
  } catch (error: any) {
    throw new Error(error.message || 'Failed to geocode address')
  }
}
