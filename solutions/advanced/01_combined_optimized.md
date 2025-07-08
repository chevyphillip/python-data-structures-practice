# Optimized Solutions: Combined Practice

## Scenario 1: Social Media Analytics

### 🟢 Basic Approach (Learning Fundamentals)

```python
posts_data = [
    "AI Update: New model released #AI #MachineLearning #Tech", "tech", 245, 38, 12,
    "Python tip: Use list comprehensions #Python #Coding #Programming", "tutorial", 189, 45, 8,
    "Coffee break thoughts #Personal #Life #Coffee", "personal", 67, 12, 3,
    "Deep learning breakthrough #AI #DeepLearning #Research", "tech", 312, 67, 23,
    "Weekend coding project #Python #WebDev #Personal", "project", 156, 34, 7
]

# Manual data conversion - educational
posts = []
for i in range(0, len(posts_data), 5):
    post = {
        "content": posts_data[i],
        "category": posts_data[i+1],
        "likes": posts_data[i+2],
        "shares": posts_data[i+3],
        "comments": posts_data[i+4]
    }
    post["total_engagement"] = post["likes"] + post["shares"] + post["comments"]
    posts.append(post)

# Find most engaging post manually
most_engaging = posts[0]
for post in posts:
    if post["total_engagement"] > most_engaging["total_engagement"]:
        most_engaging = post

# Calculate category averages manually
category_totals = {}
category_counts = {}

for post in posts:
    category = post["category"]
    engagement = post["total_engagement"]

    if category in category_totals:
        category_totals[category] += engagement
        category_counts[category] += 1
    else:
        category_totals[category] = engagement
        category_counts[category] = 1

category_stats = {}
for category in category_totals:
    category_stats[category] = category_totals[category] / category_counts[category]

# Extract hashtags manually
all_hashtags = set()
for post in posts:
    content = post["content"]
    words = content.split()
    for word in words:
        if word.startswith("#"):
            all_hashtags.add(word)
```

### 🟡 Optimized Approach (Pythonic Style)

```python
# Using list comprehension for data conversion
posts = [
    {
        "content": posts_data[i],
        "category": posts_data[i+1],
        "likes": posts_data[i+2],
        "shares": posts_data[i+3],
        "comments": posts_data[i+4],
        "total_engagement": posts_data[i+2] + posts_data[i+3] + posts_data[i+4]
    }
    for i in range(0, len(posts_data), 5)
]

# Find most engaging using max() with key
most_engaging = max(posts, key=lambda x: x["total_engagement"])

# Calculate category averages using defaultdict
from collections import defaultdict

category_data = defaultdict(list)
for post in posts:
    category_data[post["category"]].append(post["total_engagement"])

category_stats = {
    category: sum(engagements) / len(engagements)
    for category, engagements in category_data.items()
}

# Extract hashtags using set comprehension and regex
import re
all_hashtags = {
    hashtag for post in posts
    for hashtag in re.findall(r'#\w+', post["content"])
}

# Alternative: Using generator expression for memory efficiency
hashtag_generator = (
    hashtag for post in posts
    for hashtag in re.findall(r'#\w+', post["content"])
)
all_hashtags = set(hashtag_generator)
```

### 🔴 Advanced Approach (Professional Techniques)

```python
from collections import defaultdict, Counter
from itertools import groupby
from operator import itemgetter
from typing import Dict, List, Set, Tuple
import re
from dataclasses import dataclass
from statistics import mean, median, stdev

@dataclass
class SocialPost:
    """Structured representation of a social media post."""
    content: str
    category: str
    likes: int
    shares: int
    comments: int

    @property
    def total_engagement(self) -> int:
        return self.likes + self.shares + self.comments

    @property
    def hashtags(self) -> Set[str]:
        return set(re.findall(r'#\w+', self.content.lower()))

    @property
    def engagement_rate(self) -> float:
        """Simple engagement rate calculation."""
        return self.total_engagement / max(self.likes, 1)  # Avoid division by zero

class SocialMediaAnalyzer:
    """Advanced social media analytics engine."""

    def __init__(self, posts: List[SocialPost]):
        self.posts = posts
        self._category_cache = {}
        self._hashtag_cache = None

    def get_top_posts(self, n: int = 5, metric: str = 'total_engagement') -> List[SocialPost]:
        """Get top N posts by specified metric."""
        return sorted(self.posts, key=lambda p: getattr(p, metric), reverse=True)[:n]

    def analyze_by_category(self) -> Dict[str, Dict]:
        """Comprehensive category analysis with caching."""
        if self._category_cache:
            return self._category_cache

        # Group posts by category using itertools.groupby
        sorted_posts = sorted(self.posts, key=lambda p: p.category)
        category_groups = groupby(sorted_posts, key=lambda p: p.category)

        analysis = {}
        for category, posts_iter in category_groups:
            posts_list = list(posts_iter)
            engagements = [p.total_engagement for p in posts_list]

            analysis[category] = {
                'count': len(posts_list),
                'total_engagement': sum(engagements),
                'avg_engagement': mean(engagements),
                'median_engagement': median(engagements),
                'std_engagement': stdev(engagements) if len(engagements) > 1 else 0,
                'top_post': max(posts_list, key=lambda p: p.total_engagement),
                'engagement_distribution': Counter(
                    'high' if e > mean(engagements) else 'low' for e in engagements
                )
            }

        self._category_cache = analysis
        return analysis

    def get_hashtag_analytics(self) -> Dict[str, Dict]:
        """Advanced hashtag analysis."""
        if self._hashtag_cache is not None:
            return self._hashtag_cache

        # Collect all hashtags with their post contexts
        hashtag_posts = defaultdict(list)
        for post in self.posts:
            for hashtag in post.hashtags:
                hashtag_posts[hashtag].append(post)

        # Calculate metrics for each hashtag
        hashtag_analytics = {}
        for hashtag, posts_with_tag in hashtag_posts.items():
            engagements = [p.total_engagement for p in posts_with_tag]
            categories = [p.category for p in posts_with_tag]

            hashtag_analytics[hashtag] = {
                'frequency': len(posts_with_tag),
                'avg_engagement': mean(engagements),
                'total_engagement': sum(engagements),
                'categories': Counter(categories),
                'top_post': max(posts_with_tag, key=lambda p: p.total_engagement)
            }

        self._hashtag_cache = hashtag_analytics
        return hashtag_analytics

    def find_trending_topics(self, min_frequency: int = 2) -> List[Tuple[str, float]]:
        """Identify trending hashtags by engagement and frequency."""
        hashtag_analytics = self.get_hashtag_analytics()

        # Calculate trend score: frequency * avg_engagement
        trending = [
            (hashtag, data['frequency'] * data['avg_engagement'])
            for hashtag, data in hashtag_analytics.items()
            if data['frequency'] >= min_frequency
        ]

        return sorted(trending, key=itemgetter(1), reverse=True)

    def get_content_insights(self) -> Dict[str, any]:
        """Extract content insights using advanced techniques."""
        # Word frequency analysis
        all_words = []
        for post in self.posts:
            # Simple tokenization (could be enhanced with NLP libraries)
            words = re.findall(r'\b\w+\b', post.content.lower())
            all_words.extend(word for word in words if len(word) > 3)

        word_freq = Counter(all_words)

        # Engagement correlation with content length
        content_lengths = [len(post.content) for post in self.posts]
        engagements = [post.total_engagement for post in self.posts]

        # Simple correlation calculation
        n = len(content_lengths)
        if n > 1:
            mean_length = mean(content_lengths)
            mean_engagement = mean(engagements)

            correlation = sum(
                (length - mean_length) * (engagement - mean_engagement)
                for length, engagement in zip(content_lengths, engagements)
            ) / (n - 1)
        else:
            correlation = 0

        return {
            'total_posts': len(self.posts),
            'avg_content_length': mean(content_lengths),
            'most_common_words': word_freq.most_common(10),
            'length_engagement_correlation': correlation,
            'unique_hashtags': len(set().union(*(p.hashtags for p in self.posts))),
            'avg_hashtags_per_post': mean(len(p.hashtags) for p in self.posts)
        }

# Usage
raw_posts = [
    SocialPost(posts_data[i], posts_data[i+1], posts_data[i+2], posts_data[i+3], posts_data[i+4])
    for i in range(0, len(posts_data), 5)
]

analyzer = SocialMediaAnalyzer(raw_posts)

# Get comprehensive analytics
top_posts = analyzer.get_top_posts(3)
category_analysis = analyzer.analyze_by_category()
hashtag_analytics = analyzer.get_hashtag_analytics()
trending_topics = analyzer.find_trending_topics()
content_insights = analyzer.get_content_insights()

most_engaging = top_posts[0]
category_stats = {cat: data['avg_engagement'] for cat, data in category_analysis.items()}
all_hashtags = set(hashtag_analytics.keys())
```

### 🎯 Key Takeaways

- **Basic**: Manual loops teach data structure integration
- **Optimized**: `defaultdict`, `max()` with key, and comprehensions improve efficiency
- **Advanced**: `dataclasses`, `itertools.groupby`, and caching provide professional solutions
- **Performance**: Caching prevents redundant calculations
- **Scalability**: Generator expressions and efficient data structures handle large datasets

---

## Scenario 2: E-commerce Order Processing

### 🟢 Basic Approach (Learning Fundamentals)

```python
raw_orders = [
    "Alice", "Laptop", 1, 999.99,
    "Bob", "Mouse", 2, 25.99,
    "Alice", "Keyboard", 1, 79.99,
    "Charlie", "Monitor", 1, 299.99,
    "Bob", "Laptop", 1, 999.99,
    "Diana", "Mouse", 3, 25.99,
    "Alice", "Monitor", 2, 299.99
]

# Manual data conversion - educational
orders = []
for i in range(0, len(raw_orders), 4):
    order = {
        "customer": raw_orders[i],
        "product": raw_orders[i+1],
        "quantity": raw_orders[i+2],
        "price_per_item": raw_orders[i+3],
        "total": raw_orders[i+2] * raw_orders[i+3]
    }
    orders.append(order)

# Calculate customer spending manually
customer_spending = {}
for order in orders:
    customer = order["customer"]
    total = order["total"]

    if customer in customer_spending:
        customer_spending[customer] += total
    else:
        customer_spending[customer] = total

# Count product sales manually
product_sales = {}
for order in orders:
    product = order["product"]
    quantity = order["quantity"]

    if product in product_sales:
        product_sales[product] += quantity
    else:
        product_sales[product] = quantity

# Find VIP customers manually
customer_order_count = {}
for order in orders:
    customer = order["customer"]

    if customer in customer_order_count:
        customer_order_count[customer] += 1
    else:
        customer_order_count[customer] = 1

vip_customers = []
for customer, count in customer_order_count.items():
    if count > 1:
        vip_customers.append(customer)

# Find bestselling product manually
bestseller = None
max_sales = 0
for product, sales in product_sales.items():
    if sales > max_sales:
        max_sales = sales
        bestseller = product
```

### 🟡 Optimized Approach (Pythonic Style)

```python
# Using list comprehension for data conversion
orders = [
    {
        "customer": raw_orders[i],
        "product": raw_orders[i+1],
        "quantity": raw_orders[i+2],
        "price_per_item": raw_orders[i+3],
        "total": raw_orders[i+2] * raw_orders[i+3]
    }
    for i in range(0, len(raw_orders), 4)
]

# Using defaultdict for automatic initialization
from collections import defaultdict, Counter

customer_spending = defaultdict(float)
product_sales = defaultdict(int)
customer_order_count = defaultdict(int)

for order in orders:
    customer_spending[order["customer"]] += order["total"]
    product_sales[order["product"]] += order["quantity"]
    customer_order_count[order["customer"]] += 1

# Convert defaultdicts to regular dicts
customer_spending = dict(customer_spending)
product_sales = dict(product_sales)

# Find VIP customers using comprehension
vip_customers = [
    customer for customer, count in customer_order_count.items()
    if count > 1
]

# Find bestselling product using max() with key
bestseller = max(product_sales, key=product_sales.get)

# Alternative: Using Counter for more functionality
product_counter = Counter()
customer_spending_counter = Counter()

for order in orders:
    product_counter[order["product"]] += order["quantity"]
    customer_spending_counter[order["customer"]] += order["total"]

# Get top products and customers
top_products = product_counter.most_common(3)
top_customers = customer_spending_counter.most_common(3)
```

### 🔴 Advanced Approach (Professional Techniques)

```python
from collections import defaultdict, Counter, namedtuple
from itertools import groupby
from operator import itemgetter, attrgetter
from typing import Dict, List, Set, Tuple, NamedTuple
from dataclasses import dataclass
from functools import reduce
from statistics import mean, median
import json

@dataclass
class Order:
    """Structured order representation."""
    customer: str
    product: str
    quantity: int
    price_per_item: float

    @property
    def total(self) -> float:
        return self.quantity * self.price_per_item

    @property
    def revenue_category(self) -> str:
        """Categorize order by revenue."""
        if self.total >= 500:
            return "high"
        elif self.total >= 100:
            return "medium"
        else:
            return "low"

class EcommerceAnalyzer:
    """Advanced e-commerce analytics engine."""

    def __init__(self, orders: List[Order]):
        self.orders = orders
        self._customer_cache = {}
        self._product_cache = {}

    def get_customer_analytics(self) -> Dict[str, Dict]:
        """Comprehensive customer analysis with caching."""
        if self._customer_cache:
            return self._customer_cache

        # Group orders by customer using itertools.groupby
        sorted_orders = sorted(self.orders, key=attrgetter('customer'))
        customer_groups = groupby(sorted_orders, key=attrgetter('customer'))

        analytics = {}
        for customer, orders_iter in customer_groups:
            customer_orders = list(orders_iter)
            totals = [order.total for order in customer_orders]
            products = [order.product for order in customer_orders]

            analytics[customer] = {
                'order_count': len(customer_orders),
                'total_spent': sum(totals),
                'avg_order_value': mean(totals),
                'median_order_value': median(totals),
                'unique_products': len(set(products)),
                'favorite_product': Counter(products).most_common(1)[0][0],
                'customer_tier': self._calculate_customer_tier(sum(totals), len(customer_orders)),
                'orders': customer_orders
            }

        self._customer_cache = analytics
        return analytics

    def get_product_analytics(self) -> Dict[str, Dict]:
        """Advanced product performance analysis."""
        if self._product_cache:
            return self._product_cache

        # Group by product
        sorted_orders = sorted(self.orders, key=attrgetter('product'))
        product_groups = groupby(sorted_orders, key=attrgetter('product'))

        analytics = {}
        for product, orders_iter in product_groups:
            product_orders = list(orders_iter)
            quantities = [order.quantity for order in product_orders]
            revenues = [order.total for order in product_orders]
            customers = [order.customer for order in product_orders]

            analytics[product] = {
                'total_quantity_sold': sum(quantities),
                'total_revenue': sum(revenues),
                'avg_price': mean(order.price_per_item for order in product_orders),
                'order_count': len(product_orders),
                'unique_customers': len(set(customers)),
                'avg_quantity_per_order': mean(quantities),
                'revenue_per_customer': sum(revenues) / len(set(customers)),
                'top_customer': Counter(customers).most_common(1)[0][0]
            }

        self._product_cache = analytics
        return analytics

    def _calculate_customer_tier(self, total_spent: float, order_count: int) -> str:
        """Calculate customer tier based on spending and frequency."""
        if total_spent >= 1000 and order_count >= 3:
            return "platinum"
        elif total_spent >= 500 or order_count >= 2:
            return "gold"
        else:
            return "silver"

    def get_vip_customers(self, min_orders: int = 2, min_spending: float = 0) -> List[str]:
        """Identify VIP customers with flexible criteria."""
        customer_analytics = self.get_customer_analytics()

        return [
            customer for customer, data in customer_analytics.items()
            if data['order_count'] >= min_orders and data['total_spent'] >= min_spending
        ]

    def get_bestselling_products(self, metric: str = 'quantity', top_n: int = 5) -> List[Tuple[str, float]]:
        """Get bestselling products by various metrics."""
        product_analytics = self.get_product_analytics()

        metric_map = {
            'quantity': 'total_quantity_sold',
            'revenue': 'total_revenue',
            'orders': 'order_count',
            'customers': 'unique_customers'
        }

        if metric not in metric_map:
            raise ValueError(f"Metric must be one of: {list(metric_map.keys())}")

        metric_key = metric_map[metric]

        return sorted(
            [(product, data[metric_key]) for product, data in product_analytics.items()],
            key=itemgetter(1),
            reverse=True
        )[:top_n]

    def analyze_purchase_patterns(self) -> Dict[str, any]:
        """Advanced purchase pattern analysis."""
        # Revenue distribution analysis
        revenue_categories = Counter(order.revenue_category for order in self.orders)

        # Customer purchase frequency analysis
        customer_analytics = self.get_customer_analytics()
        frequency_distribution = Counter(
            data['order_count'] for data in customer_analytics.values()
        )

        # Product co-purchase analysis (simplified)
        customer_products = defaultdict(set)
        for order in self.orders:
            customer_products[order.customer].add(order.product)

        # Find customers who bought multiple products
        multi_product_customers = {
            customer: products for customer, products in customer_products.items()
            if len(products) > 1
        }

        # Calculate average basket size
        basket_sizes = [len(products) for products in customer_products.values()]

        return {
            'revenue_distribution': dict(revenue_categories),
            'frequency_distribution': dict(frequency_distribution),
            'multi_product_customers': len(multi_product_customers),
            'avg_basket_size': mean(basket_sizes),
            'total_customers': len(customer_products),
            'repeat_customer_rate': len([c for c, d in customer_analytics.items() if d['order_count'] > 1]) / len(customer_analytics),
            'cross_selling_opportunities': len(multi_product_customers) / len(customer_products)
        }

    def generate_recommendations(self) -> Dict[str, List[str]]:
        """Generate business recommendations based on analysis."""
        customer_analytics = self.get_customer_analytics()
        product_analytics = self.get_product_analytics()
        patterns = self.analyze_purchase_patterns()

        recommendations = {
            'focus_customers': [],
            'promote_products': [],
            'retention_strategies': [],
            'growth_opportunities': []
        }

        # Identify customers for targeted marketing
        silver_customers = [
            customer for customer, data in customer_analytics.items()
            if data['customer_tier'] == 'silver' and data['total_spent'] > 200
        ]
        recommendations['focus_customers'] = silver_customers[:5]

        # Products needing promotion
        low_performing = [
            product for product, data in product_analytics.items()
            if data['total_quantity_sold'] < 3
        ]
        recommendations['promote_products'] = low_performing

        # Retention strategies
        if patterns['repeat_customer_rate'] < 0.5:
            recommendations['retention_strategies'].append("Implement loyalty program")

        if patterns['avg_basket_size'] < 2:
            recommendations['retention_strategies'].append("Create product bundles")

        return recommendations

# Usage
raw_order_data = [
    "Alice", "Laptop", 1, 999.99,
    "Bob", "Mouse", 2, 25.99,
    "Alice", "Keyboard", 1, 79.99,
    "Charlie", "Monitor", 1, 299.99,
    "Bob", "Laptop", 1, 999.99,
    "Diana", "Mouse", 3, 25.99,
    "Alice", "Monitor", 2, 299.99
]

# Convert to structured orders
orders = [
    Order(raw_order_data[i], raw_order_data[i+1], raw_order_data[i+2], raw_order_data[i+3])
    for i in range(0, len(raw_order_data), 4)
]

analyzer = EcommerceAnalyzer(orders)

# Get comprehensive analytics
customer_analytics = analyzer.get_customer_analytics()
product_analytics = analyzer.get_product_analytics()
vip_customers = analyzer.get_vip_customers()
bestselling_products = analyzer.get_bestselling_products('quantity')
purchase_patterns = analyzer.analyze_purchase_patterns()
recommendations = analyzer.generate_recommendations()

# Extract specific results for compatibility
customer_spending = {customer: data['total_spent'] for customer, data in customer_analytics.items()}
product_sales = {product: data['total_quantity_sold'] for product, data in product_analytics.items()}
bestseller = bestselling_products[0][0] if bestselling_products else None
```

### 🎯 Key Takeaways

- **Basic**: Manual aggregation teaches fundamental data processing
- **Optimized**: `defaultdict` and `Counter` eliminate boilerplate code
- **Advanced**: `dataclasses`, `groupby`, and comprehensive analytics provide enterprise-level insights
- **Performance**: Caching and efficient grouping operations scale well
- **Business Value**: Advanced analytics generate actionable business recommendations

### 📊 Performance Comparison

- Manual loops: O(n) per operation, multiple passes through data
- `defaultdict`: O(1) average insertion, single pass
- `Counter`: Optimized C implementation, ~30% faster than manual counting
- `groupby`: Memory-efficient grouping, O(n log n) with sorting
- Caching: Eliminates redundant calculations for repeated queries
