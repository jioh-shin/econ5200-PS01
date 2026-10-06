[Prep] Act as a partner reviewing an analytics deliverable before it
goes to a client board. You are looking for the objection that would
embarrass us in the room.

[Request] I audited a retailer's "average basket value" metric. I found
the naive mean was inflated by a right-skewed B2B tail and by a change
in what was logged between years. I recommend the dashboard show a
trimmed mean with an explicit B2B exclusion rule. Give me the three
strongest objections to that recommendation, ordered by how likely the
client is to raise them, and for each one tell me what evidence would
settle it.

[Iterate] Be specific to this metric. Do not give me generic data
quality advice.

[Mechanism Check] For each objection, say whether it is a question
about the data, about the statistic, or about the business definition
of the metric -- these need different kinds of answer.

[Evaluate] Which single additional analysis would most reduce our
exposure?

The biggest vulnerability is that your recommendation combines two separate interventions—changing the population (exclude B2B) and changing the estimator (trimmed mean). A client can reasonably ask whether both are necessary.
Rank	Likely client objection	Mechanism	What would settle it
1	“Why are B2B transactions being excluded? Aren’t they legitimate sales?” If “average basket value” has historically meant average value across all transactions, removing large B2B baskets may look like redefining the KPI to make it more stable or attractive.	Business definition	Quantify B2B vs. consumer transactions separately: transaction count, revenue share, basket-value distribution, and operational/customer differences. Most importantly, establish whether the dashboard is intended to measure typical consumer shopping behavior or all commercial transactions. If B2B is economically a different transaction type, exclusion is defensible; otherwise, segmentation is probably better than deletion.
2	“Why a trimmed mean? What exactly are you throwing away?” Once B2B has been explicitly excluded, the client may ask why remaining high-value consumer baskets should also be trimmed. A trimmed mean can obscure genuine changes in high-value purchasing. The choice of 1%, 5%, 10%, etc. can also look arbitrary.	Statistic	Run a sensitivity table on the same B2B-excluded population: ordinary mean, median, and several symmetric trimmed means (e.g. 1%, 2.5%, 5%). Show both levels and YoY changes. Also report what fraction of revenue and transactions gets removed at each threshold. If the conclusion is stable across reasonable trims, your choice is much easier to defend.
3	“How do we know the apparent basket-value change isn’t still an artifact of the logging change?” Trimming addresses skewness; B2B exclusion addresses population composition. Neither automatically fixes a measurement-regime break. If 2025 logs basket components differently from 2024, you may still be comparing non-equivalent observations.	Data	Construct the metric using only fields/events that are definitionally comparable before and after the logging change. Ideally use an overlap period, dual logging, raw receipts/orders, or another independent transaction source to calculate old-definition and new-definition ABV on the same transactions. Estimate the size of the logging discontinuity.
The objection most likely to hurt in the room
I would prepare especially for #1. Suppose the client says:
“Our B2B customers spend real money. Why does your ‘average basket value’ suddenly pretend they don't exist?”
You don't want the answer to be “because they are outliers.” That's a statistical justification for changing a business population, which is the wrong mechanism.
The stronger answer is: the dashboard's intended construct is consumer basket behavior; B2B orders represent a distinct purchasing process, so we define the consumer ABV population explicitly and report B2B separately. If that isn't actually the intended construct, I would not recommend simply excluding B2B. I would show Consumer ABV and B2B ABV separately, with an all-transactions metric where appropriate.
Single additional analysis with the highest payoff
Do a metric bridge / decomposition analysis:
reported naive ABV → comparable-logging ABV → B2B-excluded ABV → trimmed consumer ABV.
For each step, show both the level and YoY change.
That analysis answers the board-level question your current recommendation leaves exposed:
“Which problem is actually driving the misleading number?”
For example, if naive ABV is up 14%, but harmonizing the logging definition takes that to +6%, excluding B2B takes it to +3%, and trimming changes it only to +2.8%, you have learned something important: the logging break and population definition are the substantive problems; trimming is nearly irrelevant. In that case I would probably drop the trimmed mean recommendation rather than introduce unnecessary statistical complexity.
Conversely, if trimming materially stabilizes ABV even after logging harmonization and B2B separation, you have empirical evidence that the estimator change is doing useful work rather than cosmetically suppressing the tail.



I tested the strongest objection by comparing B2B and consumer transactions separately. I found that there were only 300 B2B transactions, but their average basket value was much higher than the consumer average. Based on this check, I kept the mean after excluding B2B transactions rather than switching to a trimmed mean.
