provider "aws" {
  region = var.region
}

data "external" "trigger" {
  program = [
    "${path.module}/dirhash.sh"]

  query {
    directory = "${path.module}/../src"
  }
}

resource "null_resource" "pip" {
  triggers = {
    md5 = data.external.trigger.result["checksum"]
    requirements = base64sha256(file("${path.module}/../requirements.txt"))
  }

  provisioner "local-exec" {
    command = "rm -rf ./src"
  }
  provisioner "local-exec" {
    command = "cp -rf ../src src"
  }
  provisioner "local-exec" {
    command = "${var.pip_path} install --upgrade -r ../requirements.txt -t src"
  }
}

data "archive_file" "lambda_zip" {
  type = "zip"
  source_dir = "${path.root}/src"
  output_path = "${path.root}/lambda.zip"

  depends_on = [
    "null_resource.pip"]
}


resource "aws_iam_role" "iam_img_bot_lambda" {

  name = "iam_${var.lambda_name}"

  assume_role_policy = file("${path.module}/policy.json")
}

resource "aws_iam_role_policy_attachment" "basic_exec_role" {
  role = aws_iam_role.iam_img_bot_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "img_bot_lambda" {
  function_name = var.lambda_name
  filename = var.lambda_payload_filename

  source_code_hash = "${data.archive_file.lambda_zip.output_base64sha256}"
  timeout = var.lambda_timeout
  role = aws_iam_role.iam_img_bot_lambda.arn
  handler = var.lambda_function_handler
  runtime = var.lambda_runtime
  memory_size = var.lambda_memory
  environment {
    variables = {
      IMG_BOT_USER_NAME = var.user_name
      IMG_BOT_PASSWORD = var.password
      IMG_BOT_HASHTAGS = var.hashtags
    }
  }
}

resource "aws_cloudwatch_event_rule" "img_bot_lambda_event_rule" {
  name = "img_bot_lambda_event"
  description = "Fires every 4h"
  schedule_expression = "rate(4 hours)"
}

resource "aws_cloudwatch_event_target" "img_bot_lambda_event_target" {
  rule = aws_cloudwatch_event_rule.img_bot_lambda_event_rule.name
  target_id = "img_bot_lambda"
  arn = aws_lambda_function.img_bot_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_img_bot_lambda" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.img_bot_lambda.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.img_bot_lambda_event_rule.arn
}
