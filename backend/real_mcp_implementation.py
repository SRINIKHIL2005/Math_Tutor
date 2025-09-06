

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import aiohttp
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MCPSearchResult:
    """MCP search result structure"""
    title: str
    content: str
    url: str
    relevance_score: float
    source: str

class WebSearchMCP:
    """
    Web Search Model Context Protocol implementation
    Using multiple search backends for reliable results
    """
    
    def __init__(self):
        """Initialize the MCP web search server"""
        self.session = None
        self.search_engines = {
            'duckduckgo': self._search_duckduckgo,
            'wikipedia': self._search_wikipedia,
            'fallback': self._fallback_search
        }
        logger.info("🌐 MCP Web Search Server initialized")
    
    async def initialize(self):
        """Initialize async session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            logger.info("✅ MCP HTTP session initialized")
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
            logger.info("🧹 MCP session cleaned up")
    
    async def search(self, query: str, max_results: int = 5) -> List[MCPSearchResult]:
        """
        Main search function using MCP pattern
        Tries multiple search engines for best results
        """
        try:
            await self.initialize()
            
            logger.info(f"🔍 MCP Search: {query}")
            
            # Try search engines in order of preference
            all_results = []
            
            # 1. Try DuckDuckGo search
            try:
                ddg_results = await self._search_duckduckgo(query, max_results)
                all_results.extend(ddg_results)
                logger.info(f"DuckDuckGo found {len(ddg_results)} results")
            except Exception as e:
                logger.warning(f"DuckDuckGo search failed: {e}")
            
            # 2. Try Wikipedia search
            try:
                wiki_results = await self._search_wikipedia(query, 2)
                all_results.extend(wiki_results)
                logger.info(f"Wikipedia found {len(wiki_results)} results")
            except Exception as e:
                logger.warning(f"Wikipedia search failed: {e}")
            
            # 3. Fallback search if no results
            if not all_results:
                try:
                    fallback_results = await self._fallback_search(query, max_results)
                    all_results.extend(fallback_results)
                    logger.info(f"Fallback search found {len(fallback_results)} results")
                except Exception as e:
                    logger.warning(f"Fallback search failed: {e}")
            
            # Sort by relevance and return top results
            all_results.sort(key=lambda x: x.relevance_score, reverse=True)
            return all_results[:max_results]
            
        except Exception as e:
            logger.error(f"MCP search error: {e}")
            return []
    
    async def _search_duckduckgo(self, query: str, max_results: int) -> List[MCPSearchResult]:
        """Search using DuckDuckGo Instant Answer API"""
        try:
            # DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            async with self.session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    results = []
                    
                    # Abstract result (main answer)
                    if data.get('Abstract'):
                        results.append(MCPSearchResult(
                            title=data.get('AbstractText', 'DuckDuckGo Result'),
                            content=data.get('Abstract', ''),
                            url=data.get('AbstractURL', ''),
                            relevance_score=0.9,
                            source='duckduckgo'
                        ))
                    
                    # Related topics
                    for topic in data.get('RelatedTopics', [])[:max_results-1]:
                        if isinstance(topic, dict) and topic.get('Text'):
                            results.append(MCPSearchResult(
                                title=topic.get('FirstURL', {}).get('text', 'Related Topic'),
                                content=topic.get('Text', ''),
                                url=topic.get('FirstURL', {}).get('url', ''),
                                relevance_score=0.7,
                                source='duckduckgo'
                            ))
                    
                    return results
            
            return []
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return []
    
    async def _search_wikipedia(self, query: str, max_results: int) -> List[MCPSearchResult]:
        """Search Wikipedia for educational content"""
        try:
            # Wikipedia API search
            search_url = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
            
            # First, search for the page
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': query,
                'srlimit': max_results
            }
            
            search_api_url = "https://en.wikipedia.org/w/api.php"
            
            async with self.session.get(search_api_url, params=search_params, timeout=10) as response:
                if response.status == 200:
                    search_data = await response.json()
                    results = []
                    
                    for page in search_data.get('query', {}).get('search', []):
                        title = page.get('title', '')
                        snippet = page.get('snippet', '')
                        
                        # Get page summary
                        try:
                            summary_url = search_url.format(title.replace(' ', '_'))
                            async with self.session.get(summary_url, timeout=5) as summary_response:
                                if summary_response.status == 200:
                                    summary_data = await summary_response.json()
                                    
                                    results.append(MCPSearchResult(
                                        title=title,
                                        content=summary_data.get('extract', snippet),
                                        url=summary_data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                                        relevance_score=0.8,
                                        source='wikipedia'
                                    ))
                        except:
                            # Use snippet if summary fails
                            results.append(MCPSearchResult(
                                title=title,
                                content=snippet,
                                url=f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                                relevance_score=0.6,
                                source='wikipedia'
                            ))
                    
                    return results
            
            return []
            
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            return []
    
    async def _fallback_search(self, query: str, max_results: int) -> List[MCPSearchResult]:
        """Fallback search when other methods fail"""
        try:
            # Create synthetic educational results based on the query
            results = []
            
            # Mathematical topics
            math_topics = {
                'algebra': 'Algebraic equations and expressions involving variables',
                'calculus': 'Mathematical analysis involving derivatives and integrals',
                'geometry': 'Study of shapes, sizes, and properties of figures',
                'statistics': 'Collection, analysis, and interpretation of data',
                'trigonometry': 'Study of triangular relationships and functions'
            }
            
            query_lower = query.lower()
            
            # Check if query matches mathematical topics
            for topic, description in math_topics.items():
                if topic in query_lower or any(word in query_lower for word in topic.split()):
                    results.append(MCPSearchResult(
                        title=f"Mathematical Topic: {topic.capitalize()}",
                        content=f"{description}. This is a fundamental area of mathematics with many practical applications.",
                        url=f"https://en.wikipedia.org/wiki/{topic.capitalize()}",
                        relevance_score=0.5,
                        source='fallback'
                    ))
            
            # Generic mathematical help
            if not results:
                results.append(MCPSearchResult(
                    title="Mathematical Problem Solving",
                    content=f"This appears to be a mathematical question: '{query}'. Mathematical problem solving typically involves identifying the problem type, applying relevant formulas or methods, and working through the solution systematically.",
                    url="https://en.wikipedia.org/wiki/Problem_solving",
                    relevance_score=0.3,
                    source='fallback'
                ))
            
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Fallback search error: {e}")
            return []

class MCPServer:
    """
    Model Context Protocol Server for Math Education
    Integrates web search with educational content filtering
    """
    
    def __init__(self):
        """Initialize MCP server"""
        self.web_search = WebSearchMCP()
        self.educational_filters = self._setup_educational_filters()
        logger.info("🎓 MCP Educational Server initialized")
    
    def _setup_educational_filters(self) -> Dict[str, Any]:
        """Setup filters for educational content"""
        return {
            'math_keywords': [
                'equation', 'formula', 'theorem', 'proof', 'calculate',
                'solve', 'derivative', 'integral', 'algebra', 'geometry'
            ],
            'educational_domains': [
                'wikipedia.org', 'khanacademy.org', 'mathworld.wolfram.com',
                'brilliant.org', 'coursera.org', 'edx.org'
            ],
            'quality_indicators': [
                'step by step', 'explanation', 'example', 'solution',
                'method', 'approach', 'technique'
            ]
        }
    
    async def search_educational_content(self, query: str) -> Dict[str, Any]:
        """
        Search for educational content with MCP
        """
        try:
            # Enhance query for educational content
            educational_query = self._enhance_query_for_education(query)
            
            # Perform web search
            search_results = await self.web_search.search(educational_query, max_results=5)
            
            # Filter and rank results for educational value
            filtered_results = self._filter_educational_results(search_results)
            
            return {
                'original_query': query,
                'enhanced_query': educational_query,
                'results': [
                    {
                        'title': result.title,
                        'content': result.content,
                        'url': result.url,
                        'source': result.source,
                        'relevance': result.relevance_score
                    }
                    for result in filtered_results
                ],
                'found_in_knowledge_base': False,  # This would be True if found in vector DB
                'search_strategy': 'mcp_web_search',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"MCP educational search error: {e}")
            return {
                'error': str(e),
                'results': [],
                'timestamp': datetime.now().isoformat()
            }
    
    def _enhance_query_for_education(self, query: str) -> str:
        """Enhance query to find educational content"""
        # Add educational context to the query
        enhanced = query
        
        # Add mathematical context if not present
        if not any(keyword in query.lower() for keyword in self.educational_filters['math_keywords']):
            enhanced += " mathematics education tutorial"
        else:
            enhanced += " step by step solution explanation"
        
        return enhanced
    
    def _filter_educational_results(self, results: List[MCPSearchResult]) -> List[MCPSearchResult]:
        """Filter results for educational value"""
        filtered = []
        
        for result in results:
            educational_score = self._calculate_educational_score(result)
            
            # Only include results with decent educational value
            if educational_score >= 0.3:
                result.relevance_score = educational_score
                filtered.append(result)
        
        # Sort by educational score
        filtered.sort(key=lambda x: x.relevance_score, reverse=True)
        return filtered
    
    def _calculate_educational_score(self, result: MCPSearchResult) -> float:
        """Calculate educational value score for a result"""
        score = result.relevance_score * 0.5  # Base score
        
        # Boost for educational domains
        for domain in self.educational_filters['educational_domains']:
            if domain in result.url:
                score += 0.3
                break
        
        # Boost for quality indicators in content
        content_lower = result.content.lower()
        for indicator in self.educational_filters['quality_indicators']:
            if indicator in content_lower:
                score += 0.1
        
        # Boost for mathematical keywords
        for keyword in self.educational_filters['math_keywords']:
            if keyword in content_lower:
                score += 0.05
        
        return min(score, 1.0)  # Cap at 1.0
    
    async def cleanup(self):
        """Cleanup MCP server resources"""
        await self.web_search.cleanup()

def get_mcp_server():
    """Factory function to get MCP server instance"""
    return MCPServer()

async def test_mcp_implementation():
    """Test the MCP implementation"""
    logger.info("🧪 Testing MCP Implementation")
    
    server = get_mcp_server()
    
    # Test queries
    test_queries = [
        "solve quadratic equation",
        "calculus derivative rules", 
        "geometry area of circle",
        "linear algebra matrices"
    ]
    
    try:
        for query in test_queries:
            logger.info(f"\n--- Testing: {query} ---")
            
            result = await server.search_educational_content(query)
            
            logger.info(f"Enhanced query: {result.get('enhanced_query', 'N/A')}")
            logger.info(f"Found {len(result.get('results', []))} results")
            
            for i, res in enumerate(result.get('results', [])[:2]):  # Show first 2
                logger.info(f"Result {i+1}: {res['title'][:50]}... (score: {res['relevance']:.2f})")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
    
    finally:
        await server.cleanup()
        logger.info("✅ MCP test completed")

if __name__ == "__main__":
    asyncio.run(test_mcp_implementation())
