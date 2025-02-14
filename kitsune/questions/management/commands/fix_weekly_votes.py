import time

from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Recalculate question weekly votes."

    def handle_noargs(self, *a, **kw):
        with connection.cursor() as cursor:
            start = time.time()
            transaction.enter_transaction_management()
            transaction.managed(True)
            rows = cursor.execute(
                """
                UPDATE questions_question q
                SET num_votes_past_week = (
                    SELECT COUNT(created)
                    FROM questions_questionvote qv
                    WHERE qv.question_id = q.id
                    AND qv.created >= DATE(SUBDATE(NOW(), 7))
                );
            """
            )
            transaction.commit()
            transaction.leave_transaction_management()
            d = time.time() - start
            print("Updated %d rows in %0.3f seconds." % (rows, d))
