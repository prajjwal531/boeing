package org.prajjwal;


import org.junit.Assert;
import org.junit.Test;
import org.meghana.creditcardapi.CreditcardResource;


public class greetingTest {

	@Test
	public void testname() {

		CreditcardResource er = new CreditcardResource();
		String name=er.getData();
		Assert.assertEquals("Hello World", name);
	}
	@Test
	public void testreturnName() {
		CreditcardResource er = new CreditcardResource();
		String name=er.getName("Prajjwal");
		Assert.assertEquals("Hello Prajjwal World", name);

	}
}
