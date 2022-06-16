---
title: App Development for Laravel
summary: Learn how to build a simple PHP application based on TiDB and Laravel.
---

# App Development for Laravel

> **Note:**
>
> This document has been archived. This indicates that this document will not be updated thereafter. You can see [Developer Guide Overview](/develop/dev-guide-overview.md) for more details.

This tutorial shows you how to build a simple PHP application based on TiDB with Laravel. The sample application to build here is a simple CRM tool where you can add, query, and update customer and order information.

## Step 1. Start a TiDB cluster

Start a pseudo TiDB cluster on your local storage:

{{< copyable "" >}}

```bash
docker run -p 127.0.0.1:$LOCAL_PORT:4000 pingcap/tidb:v5.1.0
```

The above command starts a temporary and single-node cluster with mock TiKV. The cluster listens on the port `$LOCAL_PORT`. After the cluster is stopped, any changes already made to the database are not persisted.

> **Note:**
>
> To deploy a "real" TiDB cluster for production, see the following guides:
>
> + [Deploy TiDB using TiUP for On-Premises](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)
> + [Deploy TiDB on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable)
>
> You can also [use TiDB Cloud](https://pingcap.com/products/tidbcloud/), a fully-managed Database-as-a-Service (DBaaS), which offers free trial.

## Step 2. Create a database

1. In the SQL shell, create the `laravel_demo` database that your application will use:

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE laravel_demo;
    ```

2. Create a SQL user for your application:

    {{< copyable "" >}}

    ```sql
    CREATE USER <username> IDENTIFIED BY <password>;
    ```

    Take note of the username and password. You will use them in your application code when initializing the project.

3. Grant necessary permissions to the SQL user you have just created:

    {{< copyable "" >}}

    ```sql
    GRANT ALL ON laravel_demo.* TO <username>;
    ```

## Step 3. Prepare your Laravel project

1. Install Composer.

    Laravel uses [Composer](https://getcomposer.org/), a dependency manager for PHP, to manage its dependencies. Before using Laravel, make sure you have Composer installed on your machine:

    {{< copyable "" >}}

    ```bash
    brew install composer
    ```

    > **Note:**
    >
    > The installation method might vary depending on your platform. See [Installation - Linux / Unix / macOS](https://getcomposer.org/doc/00-intro.md#installation-linux-unix-macos) for more details.

2. Install Laravel.

    Download the Laravel installer and install the Laravel framework using Composer:

    {{< copyable "" >}}

    ```bash
    composer global require laravel/installer
    ```

3. Create a project.

    Now that you have Laravel installed, you can start a project using the following command:

    {{< copyable "" >}}

    ```bash
    laravel new laravel-demo
    ```

4. Edit the configuration.

    After creating your Laravel project, you need to edit the configuration file for the application to connect to TiDB:

    {{< copyable "" >}}

    ```
    DB_CONNECTION=mysql
    DB_HOST=127.0.0.1
    DB_PORT=4000
    DB_DATABASE=laravel_demo
    DB_USERNAME=root
    DB_PASSWORD=
    ```

## Step 4. Write the application logic

After you have configured the application's database connection, you can start building out the application. To write the application logic, you need to define the models, create the controller, and update the URL routes.

### Define modules

Laravel uses the [Eloquent](https://laravel.com/docs/8.x/eloquent) model, an ORM framework, to interact with the table. Models are typically placed in the `app\Models` directory. Take the following steps to create models and map the models with the corresponding table:

1. Use the `make:model` [Artisan command](https://laravel.com/docs/8.x/artisan) to generate a new model and generate a [database migration](https://laravel.com/docs/8.x/migrations):

    {{< copyable "" >}}

    ```bash
    php artisan make:model Order -m
    php artisan make:model Customer -m
    ```

    The new migration will be placed in your `database/migrations` directory.

2. Edit the `database/migrations/2021_10_08_064043_order.php` file to create the order table. File names will change over time.

    {{< copyable "" >}}

    ```php
    <?php

    use Illuminate\Database\Migrations\Migration;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    class CreateOrdersTable extends Migration
    {
        /**
        * Runs the migrations.
        *
        * @return void
        */
        public function up()
        {
            Schema::create('order', function (Blueprint $table) {
                $table->bigIncrements('oid');
                $table->bigInteger('cid');
                $table->float('price');
            });
        }

        /**
        * Reverses the migrations.
        *
        * @return void
        */
        public function down()
        {
            Schema::dropIfExists('order');
        }
    }
    ```

3. Edit the `database/migrations/2021_10_08_064056_customer.php` file to create the customer table. File names will change over time.

    {{< copyable "" >}}

    ```php
    <?php

    use Illuminate\Database\Migrations\Migration;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    class CreateCustomersTable extends Migration
    {
        /**
         * Runs the migrations.
         *
         * @return void
         */
        public function up()
        {
            Schema::create('customer', function (Blueprint $table) {
                $table->bigIncrements('cid');
                $table->string('name',100);
            });
        }

        /**
         * Reverses the migrations.
         *
         * @return void
         */
        public function down()
        {
            Schema::dropIfExists('customer');
        }
    }
    ```

4. Use the `migrate` [Artisan command](https://laravel.com/docs/8.x/artisan) to generate tables.

    {{< copyable "" >}}

    ```php
    > $ php artisan migrate
    Migration table created successfully.
    Migrating: 2014_10_12_000000_create_users_table
    Migrated:  2014_10_12_000000_create_users_table (634.92ms)
    Migrating: 2014_10_12_100000_create_password_resets_table
    Migrated:  2014_10_12_100000_create_password_resets_table (483.58ms)
    Migrating: 2019_08_19_000000_create_failed_jobs_table
    Migrated:  2019_08_19_000000_create_failed_jobs_table (456.25ms)
    Migrating: 2019_12_14_000001_create_personal_access_tokens_table
    Migrated:  2019_12_14_000001_create_personal_access_tokens_table (877.47ms)
    Migrating: 2021_10_08_081739_create_orders_table
    Migrated:  2021_10_08_081739_create_orders_table (154.53ms)
    Migrating: 2021_10_08_083522_create_customers_table
    Migrated:  2021_10_08_083522_create_customers_table (82.02ms)
    ```

5. Edit the `app/Models/Order.php` file to tell the framework which table to use for the `Order` model:

    {{< copyable "" >}}

    ```php
    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Factories\HasFactory;
    use Illuminate\Database\Eloquent\Model;

    class Order extends Model
    {
        protected $table = 'order';

        protected $primaryKey = 'oid';

        public $timestamps = false;

        protected $fillable = [
            'cid',
            'price',
        ];

        protected $guarded = [
            'oid',
        ];

        protected $casts = [
            'uid'   => 'real',
            'price' => 'float',
        ];

        use HasFactory;
    }
    ```

6. Edit the `app/Models/Customer.php` file to tell the framework which table to use for our `customer` model:

    {{< copyable "" >}}

    ```php
    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Factories\HasFactory;
    use Illuminate\Database\Eloquent\Model;

    class Customer extends Model
    {
        use HasFactory;
        protected $table = 'customer';

        protected $primaryKey = 'cid';

        public $timestamps = false;

        protected $fillable = [
            'name',
        ];

        protected $guarded = [
            'cid',
        ];

        protected $casts = [
            'name'  => 'string',
            'cid' => 'int',
        ];
    }
    ```

### Create the controller

1. To create the [controller](https://laravel.com/docs/8.x/controllers) via the command line, run the following commands:

    {{< copyable "" >}}

    ```bash
    php artisan make:controller CustomerController
    php artisan make:controller OrderController
    ```

2. Edit `app/Http/Controllers/CustomerController.php` to control the action against the `customer` table.

    {{< copyable "" >}}

    ```php
    <?php

    namespace App\Http\Controllers;

    use App\Models\Customer;
    use Illuminate\Http\Request;

    class CustomerController extends Controller
    {
        public function getByCid($cid)
        {
            $customer_info = Customer::where('cid',$cid)->get();
            if ($customer_info->count() > 0){
                return $customer_info;
            }
            return abort(404);
        }

        public function insert(Request $request) {
            return Customer::create(['name' => $request->name]);
        }
    }
    ```

3. Edit `app/Http/Controllers/OrderController.php` to control the action against the `order` table.

    {{<copyable "" >}}

    ```php
    <?php

    namespace App\Http\Controllers;

    use App\Models\Order;
    use Illuminate\Http\Request;

    class OrderController extends Controller
    {

        public function insert(Request $request) {
            return Order::create(['cid' => $request->cid, 'price' => $request->price]);
        }

        public function delete($oid)
        {
            return Order::where('oid', $oid)->delete();
        }

        public function updateByOid(Request $request, $oid)
        {
            return Order::where('oid', $oid)->update(['price' => $request->price]);
        }

        public function queryByCid(Request $request)
        {
            return Order::where('cid', $request->query('cid'))->get();
        }
    }
    ```

### Update the URL routes

URL routing allows you to configure an application to accept request URLs. Most of the [routes](https://laravel.com/docs/8.x/routing) for your application is defined in the `app/api.php` file. The simplest Laravel routes consist of a URI and a Closure callback. The `api.php` file contains all of the code for this demo.

{{< copyable "" >}}

```php
<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\customerController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::get('/customer/{id}', 'App\Http\Controllers\CustomerController@getByCid');
Route::post('/customer', 'App\Http\Controllers\CustomerController@insert');


Route::post('/order', 'App\Http\Controllers\OrderController@insert');
Route::delete('/order/{oid}', 'App\Http\Controllers\OrderController@delete');
Route::post('/order/{oid}','App\Http\Controllers\OrderController@updateByOid');
Route::get('/order','App\Http\Controllers\OrderController@queryByCid');
```

## Step 5. Run the Laravel application

If you have PHP installed locally and you would like to use PHP's built-in development server to serve your application, you can use the serve Artisan command to start a development server at `http://localhost:8000`:

{{< copyable "" >}}

```bash
php artisan serve
```

To test the application by inserting some example data, run the following commands:

{{< copyable "" >}}

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/customer' --form 'name="Peter"'

curl --location --request POST 'http://127.0.0.1:8000/api/order' --form 'cid=1' --form 'price="3.12"'

curl --location --request POST 'http://127.0.0.1:8000/api/order/1' --form 'price="312"'

curl --location --request GET 'http://127.0.0.1:8000/api/order?cid=1'
```

To verify whether the insertion is successful, execute the following statement in the SQL shell:

{{< copyable "" >}}

```sql
MySQL root@127.0.0.1:(none)> select * from laravel_demo.order;
+-----+-----+-------+
| oid | uid | price |
+-----+-----+-------+
| 1   | 1   | 312.0 |
+-----+-----+-------+
1 row in set
Time: 0.008s
```

The result above shows that the data insertion is successful.
