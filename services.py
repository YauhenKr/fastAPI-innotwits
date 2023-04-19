from database.db import table_statistic


class StatisticServices:
    @staticmethod
    async def create_update_item_in_db(
            user_id: int,
            page_id: int,
            args: dict
    ):
        update_expression = 'SET '
        expression_attribute_values = {}
        expression_attribute_names = {}

        for index, (key, value) in enumerate(args.items()):
            attr_name = f'#attrName{index}'
            attr_value = f':attrValue{index}'
            update_expression += f"{attr_name} = {attr_value}"
            expression_attribute_names[attr_name] = key
            expression_attribute_values[attr_value] = value
            if index != len(args) - 1:
                update_expression += ', '

        response = table_statistic.update_item(
            Key={'user_id': user_id, 'page_id': page_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='UPDATED_NEW'
        )

        return response

    @staticmethod
    async def get_item(user_id: int, page_id: int):
        return table_statistic.get_item(
            Key={'user_id': user_id, 'page_id': page_id}
        )

    @staticmethod
    async def create_statistic(data: dict):
        user_data = {key: data.pop(key) for key in ["user_id", "page_id"]}
        await StatisticServices.create_update_item_in_db(
            user_id=user_data.get('user_id'),
            page_id=user_data.get('page_id'),
            args=data
        )
