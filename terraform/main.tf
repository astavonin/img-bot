provider "aws" {
  region = var.region
}


resource "null_resource" "pip" {
  triggers = {
    main         = "${base64sha256(file("lambda/main.py"))}"
    requirements = "${base64sha256(file("requirements.txt"))}"
  }

  provisioner "local-exec" {
    command = "${var.pip_path} install -r ${path.root}/requirements.txt -t lambda/lib"
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.root}/src"
  output_path = "${path.root}/lambda.zip"

  depends_on = ["null_resource.pip"]
}


resource "aws_iam_role" "iam_img_bot_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = file("${path.module}/policy.json")
}

resource "aws_iam_role_policy_attachment" "basic_exec_role" {
  role = aws_iam_role.iam_img_bot_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "img_bot_lambda" {
  function_name    = var.lambda_name
  filename = var.lambda_payload_filename

  source_code_hash = filebase64sha256(var.lambda_payload_filename)
  timeout = var.lambda_timeout
  role = aws_iam_role.iam_img_bot_lambda.arn
  handler = var.lambda_function_handler
  runtime = var.lambda_runtime
  memory_size = var.lambda_memory
}
