export const truncateText = (text: string, numSymbols: number): string => {
  if (text.length <= numSymbols) {
    return text
  }
  return text.slice(0, numSymbols) + '...'
}