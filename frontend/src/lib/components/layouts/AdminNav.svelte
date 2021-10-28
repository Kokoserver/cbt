<nav class="mt-10">
  <!-- svelte-ignore a11y-invalid-attribute -->
  <a
    class="flex items-start mt-4 py-2 px-6 text-gray-500 hover:text-primary
    hover:bg-gray-700 hover:bg-opacity-25 dropdown"
    tabindex="0"
    href="#">
    <span class="mx-3">user</span>
    <ul
      tabindex="0"
      class="p-2 shadow menu dropdown-content bg-base-100 rounded-box w-52">
      <li>
        <a href="/admin/user">all user</a>
      </li>
    </ul>
  </a>
  <!-- svelte-ignore a11y-invalid-attribute -->
  <a
    class="flex items-start mt-4 py-2 px-6 hover:text-primary dropdown
    text-gray-500 hover:bg-gray-700 hover:bg-opacity-25"
    tabindex="0"
    href="#">
    <span class="mx-3">Exam</span>
    <ul
      tabindex="0"
      class="p-2 shadow menu dropdown-content bg-base-100 rounded-box w-52">
      <li>
        <a href="/admin/exam/">all</a>
      </li>
      <li>
        <a href="/admin/exam/new">create</a>
      </li>
    </ul>
  </a>
</nav>
