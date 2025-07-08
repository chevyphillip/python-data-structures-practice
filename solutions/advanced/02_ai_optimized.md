# Optimized Solutions: AI/ML Scenarios

## Scenario 1: ML Model Registry

### 🟢 Basic Approach (Learning Fundamentals)

```python
models_data = [
    {
        "name": "fraud_detector_v1",
        "type": "classification",
        "accuracy": 0.94,
        "precision": 0.89,
        "recall": 0.91,
        "last_trained": "2024-01-15",
        "features": ["transaction_amount", "merchant_type", "time_of_day", "user_history"],
        "status": "production"
    },
    {
        "name": "recommendation_engine_v2",
        "type": "recommendation",
        "accuracy": 0.87,
        "precision": 0.82,
        "recall": 0.85,
        "last_trained": "2024-02-10",
        "features": ["user_preferences", "item_features", "interaction_history"],
        "status": "production"
    },
    {
        "name": "price_predictor_v1",
        "type": "regression",
        "accuracy": 0.76,
        "precision": 0.74,
        "recall": 0.78,
        "last_trained": "2023-12-20",
        "features": ["market_conditions", "historical_prices", "volume"],
        "status": "deprecated"
    }
]

# Manual model registry creation - educational
model_registry = {}
for model in models_data:
    model_registry[model["name"]] = model

# Find best model manually
best_model = models_data[0]
for model in models_data:
    if model["accuracy"] > best_model["accuracy"]:
        best_model = model

# Group models by type manually
models_by_type = {}
for model in models_data:
    model_type = model["type"]
    if model_type in models_by_type:
        models_by_type[model_type].append(model)
    else:
        models_by_type[model_type] = [model]

# Collect all features manually
all_features = set()
for model in models_data:
    for feature in model["features"]:
        all_features.add(feature)

# Find models needing attention manually
models_need_attention = []
for model in models_data:
    if model["accuracy"] < 0.85 or model["status"] == "deprecated":
        models_need_attention.append(model["name"])
```

### 🟡 Optimized Approach (Pythonic Style)

```python
# Using dictionary comprehension for registry
model_registry = {model["name"]: model for model in models_data}

# Find best model using max() with key
best_model = max(models_data, key=lambda m: m["accuracy"])

# Group models using defaultdict
from collections import defaultdict

models_by_type = defaultdict(list)
for model in models_data:
    models_by_type[model["type"]].append(model)

# Convert to regular dict
models_by_type = dict(models_by_type)

# Collect features using set comprehension
all_features = {
    feature for model in models_data
    for feature in model["features"]
}

# Find models needing attention using comprehension
models_need_attention = [
    model["name"] for model in models_data
    if model["accuracy"] < 0.85 or model["status"] == "deprecated"
]

# Alternative: Using filter() for functional approach
models_need_attention = list(map(
    lambda m: m["name"],
    filter(lambda m: m["accuracy"] < 0.85 or m["status"] == "deprecated", models_data)
))

# Advanced: Multiple metrics analysis
def analyze_model_performance(models):
    """Analyze model performance across multiple metrics."""
    return {
        'best_accuracy': max(models, key=lambda m: m["accuracy"]),
        'best_precision': max(models, key=lambda m: m["precision"]),
        'best_recall': max(models, key=lambda m: m["recall"]),
        'avg_accuracy': sum(m["accuracy"] for m in models) / len(models),
        'production_models': [m for m in models if m["status"] == "production"]
    }

performance_analysis = analyze_model_performance(models_data)
```

### 🔴 Advanced Approach (Professional Techniques)

```python
from collections import defaultdict, Counter
from operator import itemgetter, attrgetter
from itertools import groupby
from typing import Dict, List, Set, Tuple, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import reduce, partial
import statistics

@dataclass
class MLModel:
    """Structured ML model representation with validation."""
    name: str
    type: str
    accuracy: float
    precision: float
    recall: float
    last_trained: str
    features: List[str]
    status: str

    def __post_init__(self):
        """Validate model data after initialization."""
        if not 0 <= self.accuracy <= 1:
            raise ValueError(f"Accuracy must be between 0 and 1, got {self.accuracy}")
        if self.status not in ["production", "staging", "deprecated", "development"]:
            raise ValueError(f"Invalid status: {self.status}")

    @property
    def f1_score(self) -> float:
        """Calculate F1 score from precision and recall."""
        if self.precision + self.recall == 0:
            return 0
        return 2 * (self.precision * self.recall) / (self.precision + self.recall)

    @property
    def days_since_training(self) -> int:
        """Calculate days since last training."""
        last_trained_date = datetime.strptime(self.last_trained, "%Y-%m-%d")
        return (datetime.now() - last_trained_date).days

    @property
    def needs_retraining(self) -> bool:
        """Determine if model needs retraining based on age and performance."""
        return (self.days_since_training > 90 or
                self.accuracy < 0.8 or
                self.status == "deprecated")

class MLModelRegistry:
    """Advanced ML model registry with comprehensive analytics."""

    def __init__(self, models: List[MLModel]):
        self.models = {model.name: model for model in models}
        self._performance_cache = {}
        self._feature_cache = None

    def add_model(self, model: MLModel) -> None:
        """Add model to registry with validation."""
        if model.name in self.models:
            raise ValueError(f"Model {model.name} already exists")
        self.models[model.name] = model
        self._clear_cache()

    def get_best_models(self, metric: str = 'accuracy', n: int = 3) -> List[MLModel]:
        """Get top N models by specified metric."""
        if metric not in ['accuracy', 'precision', 'recall', 'f1_score']:
            raise ValueError(f"Invalid metric: {metric}")

        return sorted(
            self.models.values(),
            key=lambda m: getattr(m, metric),
            reverse=True
        )[:n]

    def analyze_by_type(self) -> Dict[str, Dict]:
        """Comprehensive analysis grouped by model type."""
        if 'by_type' in self._performance_cache:
            return self._performance_cache['by_type']

        # Group models by type using itertools.groupby
        sorted_models = sorted(self.models.values(), key=attrgetter('type'))
        type_groups = groupby(sorted_models, key=attrgetter('type'))

        analysis = {}
        for model_type, models_iter in type_groups:
            models_list = list(models_iter)
            accuracies = [m.accuracy for m in models_list]
            f1_scores = [m.f1_score for m in models_list]

            analysis[model_type] = {
                'count': len(models_list),
                'avg_accuracy': statistics.mean(accuracies),
                'median_accuracy': statistics.median(accuracies),
                'std_accuracy': statistics.stdev(accuracies) if len(accuracies) > 1 else 0,
                'avg_f1': statistics.mean(f1_scores),
                'best_model': max(models_list, key=attrgetter('accuracy')),
                'production_count': len([m for m in models_list if m.status == 'production']),
                'needs_retraining': [m.name for m in models_list if m.needs_retraining]
            }

        self._performance_cache['by_type'] = analysis
        return analysis

    def get_feature_analytics(self) -> Dict[str, Dict]:
        """Advanced feature usage analytics."""
        if self._feature_cache is not None:
            return self._feature_cache

        # Collect feature usage statistics
        feature_models = defaultdict(list)
        for model in self.models.values():
            for feature in model.features:
                feature_models[feature].append(model)

        feature_analytics = {}
        for feature, models_using in feature_models.items():
            accuracies = [m.accuracy for m in models_using]
            model_types = [m.type for m in models_using]

            feature_analytics[feature] = {
                'usage_count': len(models_using),
                'avg_accuracy': statistics.mean(accuracies),
                'model_types': Counter(model_types),
                'best_performing_model': max(models_using, key=attrgetter('accuracy')),
                'production_usage': len([m for m in models_using if m.status == 'production'])
            }

        self._feature_cache = feature_analytics
        return feature_analytics

    def recommend_features(self, target_type: str) -> List[Tuple[str, float]]:
        """Recommend features for a model type based on performance correlation."""
        feature_analytics = self.get_feature_analytics()

        # Filter features used in target model type and rank by performance
        recommendations = []
        for feature, data in feature_analytics.items():
            if target_type in data['model_types']:
                # Weight by usage frequency and average accuracy
                score = data['avg_accuracy'] * (data['usage_count'] / len(self.models))
                recommendations.append((feature, score))

        return sorted(recommendations, key=itemgetter(1), reverse=True)

    def get_retraining_schedule(self) -> Dict[str, List[str]]:
        """Generate retraining schedule based on model age and performance."""
        schedule = {
            'urgent': [],      # Needs immediate retraining
            'soon': [],        # Needs retraining within 30 days
            'monitor': [],     # Monitor closely
            'stable': []       # Performing well
        }

        for model in self.models.values():
            if model.accuracy < 0.7 or model.status == 'deprecated':
                schedule['urgent'].append(model.name)
            elif model.needs_retraining:
                schedule['soon'].append(model.name)
            elif model.days_since_training > 60:
                schedule['monitor'].append(model.name)
            else:
                schedule['stable'].append(model.name)

        return schedule

    def generate_model_report(self) -> Dict[str, any]:
        """Generate comprehensive model registry report."""
        all_models = list(self.models.values())

        return {
            'total_models': len(all_models),
            'by_status': Counter(m.status for m in all_models),
            'by_type': Counter(m.type for m in all_models),
            'performance_summary': {
                'avg_accuracy': statistics.mean(m.accuracy for m in all_models),
                'avg_precision': statistics.mean(m.precision for m in all_models),
                'avg_recall': statistics.mean(m.recall for m in all_models),
                'avg_f1': statistics.mean(m.f1_score for m in all_models)
            },
            'feature_diversity': len(self.get_feature_analytics()),
            'retraining_needed': len([m for m in all_models if m.needs_retraining]),
            'oldest_model': min(all_models, key=attrgetter('last_trained')),
            'newest_model': max(all_models, key=attrgetter('last_trained'))
        }

    def _clear_cache(self) -> None:
        """Clear performance caches when registry is modified."""
        self._performance_cache.clear()
        self._feature_cache = None

# Usage
models = [MLModel(**model_data) for model_data in models_data]
registry = MLModelRegistry(models)

# Get comprehensive analytics
best_models = registry.get_best_models('f1_score', 3)
type_analysis = registry.analyze_by_type()
feature_analytics = registry.get_feature_analytics()
feature_recommendations = registry.recommend_features('classification')
retraining_schedule = registry.get_retraining_schedule()
model_report = registry.generate_model_report()

# Extract results for compatibility
best_model = best_models[0]
models_by_type = {
    model_type: [m.name for m in data['best_model']]
    for model_type, data in type_analysis.items()
}
all_features = set(feature_analytics.keys())
models_need_attention = retraining_schedule['urgent'] + retraining_schedule['soon']
```

### 🎯 Key Takeaways

- **Basic**: Manual operations teach ML model management fundamentals
- **Optimized**: `max()` with key, comprehensions, and `defaultdict` improve efficiency
- **Advanced**: `dataclasses`, comprehensive analytics, and caching provide production-ready solutions
- **ML-Specific**: F1 score calculation, retraining schedules, and feature analytics
- **Scalability**: Caching and efficient data structures handle large model registries

---

## Scenario 2: Data Pipeline Management

### 🟢 Basic Approach (Learning Fundamentals)

```python
pipeline_logs = [
    {"pipeline": "customer_data_prep", "step": "data_ingestion", "status": "success", "records": 10000, "errors": 0},
    {"pipeline": "customer_data_prep", "step": "data_cleaning", "status": "success", "records": 9987, "errors": 13},
    {"pipeline": "customer_data_prep", "step": "feature_engineering", "status": "success", "records": 9987, "errors": 0},
    {"pipeline": "fraud_detection_prep", "step": "data_ingestion", "status": "failed", "records": 0, "errors": 1},
    {"pipeline": "fraud_detection_prep", "step": "data_cleaning", "status": "skipped", "records": 0, "errors": 0},
    {"pipeline": "product_analytics", "step": "data_ingestion", "status": "success", "records": 5000, "errors": 0},
    {"pipeline": "product_analytics", "step": "data_cleaning", "status": "warning", "records": 4950, "errors": 50}
]

# Manual grouping by pipeline - educational
logs_by_pipeline = {}
for log in pipeline_logs:
    pipeline = log["pipeline"]
    if pipeline in logs_by_pipeline:
        logs_by_pipeline[pipeline].append(log)
    else:
        logs_by_pipeline[pipeline] = [log]

# Calculate success rate manually
pipeline_health = {}
for pipeline, logs in logs_by_pipeline.items():
    total_steps = len(logs)
    successful_steps = 0
    for log in logs:
        if log["status"] == "success":
            successful_steps += 1

    pipeline_health[pipeline] = successful_steps / total_steps if total_steps > 0 else 0

# Find pipelines with errors manually
error_pipelines = []
for log in pipeline_logs:
    if log["errors"] > 0 and log["pipeline"] not in error_pipelines:
        error_pipelines.append(log["pipeline"])

# Calculate totals manually
total_records = 0
total_errors = 0
for log in pipeline_logs:
    total_records += log["records"]
    total_errors += log["errors"]

# Find unique steps manually
all_steps = set()
for log in pipeline_logs:
    all_steps.add(log["step"])
```

### 🟡 Optimized Approach (Pythonic Style)

```python
from collections import defaultdict, Counter

# Group logs using defaultdict
logs_by_pipeline = defaultdict(list)
for log in pipeline_logs:
    logs_by_pipeline[log["pipeline"]].append(log)

# Convert to regular dict
logs_by_pipeline = dict(logs_by_pipeline)

# Calculate success rate using comprehensions
pipeline_health = {
    pipeline: sum(1 for log in logs if log["status"] == "success") / len(logs)
    for pipeline, logs in logs_by_pipeline.items()
}

# Find error pipelines using set comprehension
error_pipelines = list({
    log["pipeline"] for log in pipeline_logs if log["errors"] > 0
})

# Calculate totals using sum() with generator expressions
total_records = sum(log["records"] for log in pipeline_logs)
total_errors = sum(log["errors"] for log in pipeline_logs)

# Get unique steps using set comprehension
all_steps = {log["step"] for log in pipeline_logs}

# Advanced: Status distribution analysis
status_distribution = Counter(log["status"] for log in pipeline_logs)

# Pipeline efficiency metrics
pipeline_efficiency = {
    pipeline: {
        'total_records': sum(log["records"] for log in logs),
        'total_errors': sum(log["errors"] for log in logs),
        'error_rate': sum(log["errors"] for log in logs) / max(sum(log["records"] for log in logs), 1),
        'steps_completed': len(logs),
        'success_rate': sum(1 for log in logs if log["status"] == "success") / len(logs)
    }
    for pipeline, logs in logs_by_pipeline.items()
}
```

### 🔴 Advanced Approach (Professional Techniques)

```python
from collections import defaultdict, Counter, namedtuple
from itertools import groupby
from operator import itemgetter, attrgetter
from typing import Dict, List, Set, Tuple, Optional, Enum
from dataclasses import dataclass, field
from datetime import datetime
from functools import reduce
import statistics
from enum import Enum

class PipelineStatus(Enum):
    SUCCESS = "success"
    WARNING = "warning"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class PipelineLog:
    """Structured pipeline log entry."""
    pipeline: str
    step: str
    status: PipelineStatus
    records: int
    errors: int
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Validate log entry after initialization."""
        if self.records < 0:
            raise ValueError("Records count cannot be negative")
        if self.errors < 0:
            raise ValueError("Error count cannot be negative")
        if isinstance(self.status, str):
            self.status = PipelineStatus(self.status)

    @property
    def error_rate(self) -> float:
        """Calculate error rate for this log entry."""
        return self.errors / max(self.records, 1)

    @property
    def is_healthy(self) -> bool:
        """Determine if this step is healthy."""
        return self.status == PipelineStatus.SUCCESS and self.error_rate < 0.01

class DataPipelineMonitor:
    """Advanced data pipeline monitoring and analytics system."""

    def __init__(self, logs: List[PipelineLog]):
        self.logs = logs
        self._pipeline_cache = {}
        self._step_cache = {}
        self._health_cache = None

    def get_pipeline_analytics(self) -> Dict[str, Dict]:
        """Comprehensive pipeline-level analytics with caching."""
        if self._pipeline_cache:
            return self._pipeline_cache

        # Group logs by pipeline using itertools.groupby
        sorted_logs = sorted(self.logs, key=attrgetter('pipeline'))
        pipeline_groups = groupby(sorted_logs, key=attrgetter('pipeline'))

        analytics = {}
        for pipeline, logs_iter in pipeline_groups:
            pipeline_logs = list(logs_iter)

            # Calculate various metrics
            total_records = sum(log.records for log in pipeline_logs)
            total_errors = sum(log.errors for log in pipeline_logs)
            success_count = sum(1 for log in pipeline_logs if log.status == PipelineStatus.SUCCESS)

            # Step completion analysis
            step_statuses = Counter(log.status for log in pipeline_logs)
            unique_steps = {log.step for log in pipeline_logs}

            analytics[pipeline] = {
                'total_steps': len(pipeline_logs),
                'unique_steps': len(unique_steps),
                'success_rate': success_count / len(pipeline_logs),
                'total_records_processed': total_records,
                'total_errors': total_errors,
                'overall_error_rate': total_errors / max(total_records, 1),
                'step_distribution': dict(step_statuses),
                'health_score': self._calculate_health_score(pipeline_logs),
                'bottleneck_steps': self._identify_bottlenecks(pipeline_logs),
                'completion_status': self._get_completion_status(pipeline_logs)
            }

        self._pipeline_cache = analytics
        return analytics

    def get_step_analytics(self) -> Dict[str, Dict]:
        """Step-level performance analytics across all pipelines."""
        if self._step_cache:
            return self._step_cache

        # Group by step across all pipelines
        sorted_logs = sorted(self.logs, key=attrgetter('step'))
        step_groups = groupby(sorted_logs, key=attrgetter('step'))

        analytics = {}
        for step, logs_iter in step_groups:
            step_logs = list(logs_iter)

            # Performance metrics
            records_processed = [log.records for log in step_logs]
            error_rates = [log.error_rate for log in step_logs]
            success_rate = sum(1 for log in step_logs if log.status == PipelineStatus.SUCCESS) / len(step_logs)

            analytics[step] = {
                'execution_count': len(step_logs),
                'pipelines_using': len({log.pipeline for log in step_logs}),
                'success_rate': success_rate,
                'avg_records_processed': statistics.mean(records_processed),
                'median_records_processed': statistics.median(records_processed),
                'avg_error_rate': statistics.mean(error_rates),
                'reliability_score': success_rate * (1 - statistics.mean(error_rates)),
                'most_problematic_pipeline': self._find_most_problematic_pipeline(step_logs)
            }

        self._step_cache = analytics
        return analytics

    def _calculate_health_score(self, logs: List[PipelineLog]) -> float:
        """Calculate overall health score for a pipeline (0-1)."""
        if not logs:
            return 0.0

        # Weight different factors
        success_weight = 0.4
        error_weight = 0.3
        completion_weight = 0.3

        success_rate = sum(1 for log in logs if log.status == PipelineStatus.SUCCESS) / len(logs)
        avg_error_rate = statistics.mean(log.error_rate for log in logs)
        completion_rate = len([log for log in logs if log.status != PipelineStatus.SKIPPED]) / len(logs)

        health_score = (
            success_rate * success_weight +
            (1 - avg_error_rate) * error_weight +
            completion_rate * completion_weight
        )

        return min(max(health_score, 0.0), 1.0)

    def _identify_bottlenecks(self, logs: List[PipelineLog]) -> List[str]:
        """Identify bottleneck steps in a pipeline."""
        # Steps with high error rates or failures
        bottlenecks = []
        for log in logs:
            if (log.status in [PipelineStatus.FAILED, PipelineStatus.WARNING] or
                log.error_rate > 0.05):
                bottlenecks.append(log.step)

        return list(set(bottlenecks))

    def _get_completion_status(self, logs: List[PipelineLog]) -> str:
        """Determine overall completion status of a pipeline."""
        statuses = [log.status for log in logs]

        if PipelineStatus.FAILED in statuses:
            return "failed"
        elif PipelineStatus.WARNING in statuses:
            return "warning"
        elif all(status == PipelineStatus.SUCCESS for status in statuses):
            return "success"
        else:
            return "partial"

    def _find_most_problematic_pipeline(self, step_logs: List[PipelineLog]) -> str:
        """Find pipeline with most issues for a specific step."""
        pipeline_issues = defaultdict(int)

        for log in step_logs:
            if log.status != PipelineStatus.SUCCESS:
                pipeline_issues[log.pipeline] += 1

        if not pipeline_issues:
            return "none"

        return max(pipeline_issues.items(), key=itemgetter(1))[0]

    def get_system_health_report(self) -> Dict[str, any]:
        """Generate comprehensive system health report."""
        pipeline_analytics = self.get_pipeline_analytics()
        step_analytics = self.get_step_analytics()

        # Overall system metrics
        all_health_scores = [data['health_score'] for data in pipeline_analytics.values()]
        total_records = sum(data['total_records_processed'] for data in pipeline_analytics.values())
        total_errors = sum(data['total_errors'] for data in pipeline_analytics.values())

        # Identify critical issues
        failed_pipelines = [
            pipeline for pipeline, data in pipeline_analytics.items()
            if data['completion_status'] == 'failed'
        ]

        low_performing_steps = [
            step for step, data in step_analytics.items()
            if data['success_rate'] < 0.8
        ]

        return {
            'system_health_score': statistics.mean(all_health_scores) if all_health_scores else 0,
            'total_pipelines': len(pipeline_analytics),
            'total_steps_executed': len(self.logs),
            'total_records_processed': total_records,
            'total_errors': total_errors,
            'system_error_rate': total_errors / max(total_records, 1),
            'failed_pipelines': failed_pipelines,
            'low_performing_steps': low_performing_steps,
            'healthiest_pipeline': max(pipeline_analytics.items(), key=lambda x: x[1]['health_score'])[0],
            'most_reliable_step': max(step_analytics.items(), key=lambda x: x[1]['reliability_score'])[0],
            'recommendations': self._generate_recommendations(pipeline_analytics, step_analytics)
        }

    def _generate_recommendations(self, pipeline_analytics: Dict, step_analytics: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []

        # Pipeline-level recommendations
        for pipeline, data in pipeline_analytics.items():
            if data['health_score'] < 0.7:
                recommendations.append(f"Review and optimize {pipeline} pipeline (health score: {data['health_score']:.2f})")

            if data['overall_error_rate'] > 0.05:
                recommendations.append(f"Investigate high error rate in {pipeline} ({data['overall_error_rate']:.1%})")

        # Step-level recommendations
        for step, data in step_analytics.items():
            if data['success_rate'] < 0.8:
                recommendations.append(f"Improve reliability of {step} step (success rate: {data['success_rate']:.1%})")

        # System-level recommendations
        if len([p for p, d in pipeline_analytics.items() if d['completion_status'] == 'failed']) > 0:
            recommendations.append("Implement better error handling and recovery mechanisms")

        return recommendations

# Usage
raw_logs = [
    {"pipeline": "customer_data_prep", "step": "data_ingestion", "status": "success", "records": 10000, "errors": 0},
    {"pipeline": "customer_data_prep", "step": "data_cleaning", "status": "success", "records": 9987, "errors": 13},
    {"pipeline": "customer_data_prep", "step": "feature_engineering", "status": "success", "records": 9987, "errors": 0},
    {"pipeline": "fraud_detection_prep", "step": "data_ingestion", "status": "failed", "records": 0, "errors": 1},
    {"pipeline": "fraud_detection_prep", "step": "data_cleaning", "status": "skipped", "records": 0, "errors": 0},
    {"pipeline": "product_analytics", "step": "data_ingestion", "status": "success", "records": 5000, "errors": 0},
    {"pipeline": "product_analytics", "step": "data_cleaning", "status": "warning", "records": 4950, "errors": 50}
]

# Convert to structured logs
structured_logs = [PipelineLog(**log_data) for log_data in raw_logs]
monitor = DataPipelineMonitor(structured_logs)

# Get comprehensive analytics
pipeline_analytics = monitor.get_pipeline_analytics()
step_analytics = monitor.get_step_analytics()
health_report = monitor.get_system_health_report()

# Extract results for compatibility
logs_by_pipeline = defaultdict(list)
for log in structured_logs:
    logs_by_pipeline[log.pipeline].append(log)

pipeline_health = {pipeline: data['health_score'] for pipeline, data in pipeline_analytics.items()}
error_pipelines = [pipeline for pipeline, data in pipeline_analytics.items() if data['total_errors'] > 0]
total_records = health_report['total_records_processed']
total_errors = health_report['total_errors']
all_steps = set(step_analytics.keys())
```

### 🎯 Key Takeaways

- **Basic**: Manual grouping and calculations teach pipeline monitoring fundamentals
- **Optimized**: `defaultdict`, comprehensions, and `Counter` streamline data processing
- **Advanced**: `dataclasses`, `Enum`, comprehensive analytics provide production monitoring
- **ML Pipeline Specific**: Health scores, bottleneck identification, and system recommendations
- **Scalability**: Caching and efficient grouping handle large-scale pipeline monitoring

### 📊 Performance & Business Value

- **Health Scoring**: Quantifies pipeline reliability for SLA monitoring
- **Bottleneck Identification**: Pinpoints optimization opportunities
- **Predictive Insights**: Identifies pipelines likely to fail
- **Resource Optimization**: Guides infrastructure allocation decisions
- **Automated Recommendations**: Reduces manual monitoring overhead
